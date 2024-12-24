from fastapi import FastAPI
import uvicorn
from api import router as api_router
from core.config import settings
from redis_client import redis_cli

import sys
sys.path.insert(0, ".")

main_app = FastAPI()
main_app.include_router(api_router)

redis_cli.ping()

if __name__ == '__main__':
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True
    )




