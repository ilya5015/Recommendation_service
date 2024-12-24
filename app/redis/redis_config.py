import redis
from app.core.config import settings

class RedisClient:
    def __init__(self):
        self.client = redis.Redis(host=settings.redis_host, port=settings.redis_port)

    def get_client(self):
        return self.client

redis_client_instance = RedisClient().get_client()