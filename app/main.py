import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from fastapi import FastAPI
import uvicorn
from api import router as api_router
from core.config import settings
from redis_client.redis_config import initialize_db
from contextlib import asynccontextmanager
from recommender_service.recommendation_model import RecommendationModel
from recommender_service.scheduler import ModelScheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        app.state.redis = initialize_db()
        
        model = RecommendationModel()
        
        scheduler = ModelScheduler(model, app.state.redis, settings.db.database_url)
        
        scheduler.start()
        yield
    finally:
        scheduler.stop()
        app.state.redis.close()
        


main_app = FastAPI(lifespan=lifespan)

main_app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run("main:main_app", host=settings.run.host, port=settings.run.port, reload=False)





