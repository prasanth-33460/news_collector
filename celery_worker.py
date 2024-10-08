from celeryconfig import app
from database import Session, Article
from classifier import classify_article
from sqlalchemy.exc import IntegrityError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.task
def process_article(article):
    session = Session()
    
    try:
        category = classify_article(article)
        
        existing_article = session.query(Article).filter_by(url=article['url']).first()
        if existing_article:
            logger.info(f"Article already exists: {article['title']}")
            return
        
        new_article = Article(
            title=article['title'],
            content=article['content'],
            published=article['published'],
            url=article['url'],
            category=category
        )
        
        session.add(new_article)
        session.commit()
        logger.info(f"Article added: {article['title']}")
    
    except IntegrityError:
        session.rollback()
        logger.error(f"IntegrityError: Article '{article['title']}' already exists.")
    
    except Exception as e:
        session.rollback()
        logger.error(f"Error processing article '{article['title']}': {str(e)}")
    
    finally:
        session.close()