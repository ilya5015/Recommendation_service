import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from fastapi import FastAPI
import uvicorn
from api import router as api_router
from core.config import settings
from contextlib import asynccontextmanager
from services.etl_service.etl_pipeline_schedule import start_etl_pipeline

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print('ETL process start')
        start_etl_pipeline()
        yield
    finally:
        print('ETL process stopped')


main_app = FastAPI(lifespan=lifespan)

main_app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=False
    )





