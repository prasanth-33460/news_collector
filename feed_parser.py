import feedparser
from datetime import datetime
from database import Article, Session    

rss_feeds = [
    "http://rss.cnn.com/rss/cnn_topstories.rss",
    "http://qz.com/feed",
    "http://feeds.foxnews.com/foxnews/politics",
    "http://feeds.reuters.com/reuters/businessNews",
    "http://feeds.feedburner.com/NewshourWorld",
    "https://feeds.bbci.co.uk/news/world/asia/india/rss.xml"
]

def parse_feed(feed_url):
    feed = feedparser.parse(feed_url)
    articles = []
    for entry in feed.entries:
        published_parsed = entry.get('published_parsed', None)
        if published_parsed is not None:
            published = datetime(*published_parsed[:6])
        else:
            published = None  

        articles.append({
            'title': entry.title,
            'content': entry.get('summary', ''),  
            'published': published,
            'url': entry.link,
            'category': entry.get('category', 'General')  
        })
    return articles

def collect_articles():
    all_articles = []
    for feed_url in rss_feeds:
        articles = parse_feed(feed_url)
        all_articles.extend(articles)
    return all_articles

def insert_articles(articles):
    session = Session()  
    for article in articles:
        new_article = Article(
            title=article['title'],
            content=article['content'],
            published=article['published'],  
            url=article['url'],
            category=article.get('category')  
        )
        session.add(new_article)
    session.commit()  
    print(f"Inserted {len(articles)} articles into the database.")
    session.close()  

if __name__ == "__main__":
    articles = collect_articles()
    insert_articles(articles)