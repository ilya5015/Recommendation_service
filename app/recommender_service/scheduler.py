from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import time

class ModelScheduler:
    def __init__(self, model, redis_client):
        self.model = model  # экземпляр рекомендательной модели
        self.redis_client = redis_client  # клиент Redis
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(
            self.run_model,
            trigger=IntervalTrigger(seconds=5),
            id='model_recommendation_job',
            replace_existing=True
        )
        

    def run_model(self):
        #self.model.fit() # Тренировка модели
        #recommendations = self.model.recommend()  # Вызов рекомендаций
        
        # Сохранение рекомендаций в Redis
        #self.redis_client.set('recommendations', recommendations)

        print("Рекомендации обновлены и сохранены в Redis.")

    def start(self):
        self.scheduler.start()

    def stop(self):
        self.scheduler.shutdown()