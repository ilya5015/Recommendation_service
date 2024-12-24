from fastapi import FastAPI
import uvicorn
from api import router as api_router
from core.config import settings
from services.etl_service.etl_pipeline import start_etl_pipeline

import sys
sys.path.insert(0, ".")

main_app = FastAPI()

main_app.include_router(api_router)

@main_app.on_event('startup')
def startup_event():
    start_etl_pipeline()

if __name__ == '__main__':
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True
    )




