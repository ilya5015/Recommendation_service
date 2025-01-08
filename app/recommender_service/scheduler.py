from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import time
from .ETL import ETL
import json

class ModelScheduler:
    def __init__(self, model, redis_client, database_url):
        self.model = model  # экземпляр рекомендательной модели
        self.redis_client = redis_client  # клиент Redis
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(
            self.run_task,
            trigger=IntervalTrigger(minutes=30),
            id='model_recommendation_job',
            replace_existing=True
        )
        self.database_url = database_url    

    def run_task(self):
        etl = ETL(self.database_url)
        orders_df = etl.run_pipeline()
        self.model.fit(orders_df)
        predictions = self.model.recommend_all()
        for row in predictions:
            user_id = row.user_id
            product_ids = [recommendation.product_id for recommendation in row.recommendations]
            print(product_ids)
            self.redis_client.set(user_id, json.dumps(product_ids))


    def start(self):
        self.run_task()
        self.scheduler.start()

    def stop(self):
        self.scheduler.shutdown()