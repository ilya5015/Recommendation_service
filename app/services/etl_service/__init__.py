from ETLService import ETLService
from app.redis.redis_config import redis_client_instance as redis_client

etl_service = ETLService(redis_client)