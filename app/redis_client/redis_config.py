import redis

import sys
sys.path.append('/')

from app.core.config import settings


def initialize_db():
    redis_cli = redis.Redis(
        host=settings.db.redis_host,
        port=settings.db.redis_port,
        decode_responses=True
    )

    return redis_cli