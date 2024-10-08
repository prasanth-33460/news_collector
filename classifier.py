import spacy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Article, Base  

nlp = spacy.load("en_core_web_sm")

CATEGORIES = {
    "terrorism": ["terror", "bombing", "attack", "riot"],
    "positive": ["success", "happy", "uplifting", "positive"],
    "natural_disasters": ["earthquake", "hurricane", "flood", "disaster"]
}

def classify_article(article):
    doc = nlp(article['content']) 
    for category, keywords in CATEGORIES.items():
        if any(keyword in doc.text.lower() for keyword in keywords):
            return category
    return "others"

def classify_articles():
    engine = create_engine("postgresql://postgres:1234@localhost/newsdb")
    Session = sessionmaker(bind=engine)
    session = Session()
    
    articles = session.query(Article).all()
    
    for article in articles:
        category = classify_article({'content': article.content})  
        article.category = category  
    
    session.commit()
    session.close()

if __name__ == "__main__":
    classify_articles()