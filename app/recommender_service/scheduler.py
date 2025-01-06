from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import time
from .ETL import ETL

class ModelScheduler:
    def __init__(self, model, redis_client):
        self.model = model  # экземпляр рекомендательной модели
        self.redis_client = redis_client  # клиент Redis
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(
            self.run_task,
            trigger=IntervalTrigger(seconds=5),
            id='model_recommendation_job',
            replace_existing=True
        )
        

    def run_task(self):
        #self.model.fit() # Тренировка модели
        #recommendations = self.model.recommend()  # Вызов рекомендаций
        
        # Сохранение рекомендаций в Redis
        #self.redis_client.set('recommendations', recommendations)
        etl = ETL('')
        etl.run_pipeline()

    def start(self):
        self.scheduler.start()

    def stop(self):
        self.scheduler.shutdown()