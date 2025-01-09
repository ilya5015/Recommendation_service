from fastapi import APIRouter, HTTPException, Depends, FastAPI, Request
from app.controllers.recommendations_controller import RecommendationsController

router = APIRouter(prefix='/recommendations')

def get_redis(request: Request):
    return request.app.state.redis

@router.get("/get_recommendations")
async def get_recommendation(user_id:int, redis=Depends(get_redis)):
    recommendations_controller = RecommendationsController(redis)
    recommendations = recommendations_controller.get_recommendations(user_id)
    if recommendations is None:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return {"user_id": user_id, "recommendations": recommendations}