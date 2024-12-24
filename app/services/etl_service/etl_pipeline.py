import schedule
import time
from app.redis_client import redis_cli
from app.services.etl_service.ETLService import ETLService

etl = ETLService(redis_cli)

def etl_pipeline():
    print('pipeline pending')
    etl.run_etl('')
def start_etl_pipeline():
    schedule.every(3).seconds.do(etl_pipeline)
    while True:
        schedule.run_pending()
        time.sleep(1)
