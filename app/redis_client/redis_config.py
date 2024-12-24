import redis

class RedisClient:
    def __init__(self, settings):
        self.client = redis.Redis(host=settings.redis_host, port=settings.redis_port)

    def get_client(self):
        return self.client

