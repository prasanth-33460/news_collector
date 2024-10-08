from celery import Celery

app = Celery('news_processor', broker='redis://localhost:6379/0')

app.conf.update(
    task_routes={
        'celery_worker.process_article': {'queue': 'news_queue'}
    },
    task_default_queue='news_queue'  
)