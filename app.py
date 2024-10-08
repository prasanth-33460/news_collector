from celery_worker import process_article
from database import Session, Article

def load_articles_from_db():
    session = Session()
    try:
        articles = session.query(Article).all()
        return [
            {
                'title': article.title,
                'content': article.content,
                'published': article.published,
                'url': article.url,
            }
            for article in articles
        ]
    except Exception as e:
        print(f"Error loading articles from database: {str(e)}")
        return []
    finally:
        session.close()

def send_to_queue(articles):
    for article in articles:
        print(f"Sending article to queue: {article['title']}")
        process_article.apply_async((article,), queue='news_queue')

def main():
    articles = load_articles_from_db()

    if not articles:
        print("No articles found in the database.")
        return

    send_to_queue(articles)

if __name__ == "__main__":
    main()