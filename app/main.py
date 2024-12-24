from fastapi import FastAPI
import uvicorn
from api import router as api_router
from core.config import settings
from services.etl_service.ETLService import ETLService
from redis_client.redis_config import RedisClient

redis_client_instance = RedisClient(settings.db).get_client()
etl_service = ETLService(redis_client_instance)

main_app = FastAPI()
main_app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True
    )


