from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import time
from .ETL import ETL

class ModelScheduler:
    def __init__(self, model, redis_client, database_url):
        self.model = model  # экземпляр рекомендательной модели
        self.redis_client = redis_client  # клиент Redis
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(
            self.run_task,
            trigger=IntervalTrigger(seconds=5),
            id='model_recommendation_job',
            replace_existing=True
        )
        self.database_url = database_url
        

    def run_task(self):
        etl = ETL(self.database_url)
        loaded_data = etl.run_pipeline()

    def start(self):
        self.scheduler.start()

    def stop(self):
        self.scheduler.shutdown()