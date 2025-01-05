from fastapi import APIRouter, HTTPException, Depends, FastAPI, Request

router = APIRouter(prefix='/recommendations')

def get_redis(request: Request):
    return request.app.state.redis

@router.get("/get_recommendations")
async def get_recommendation(user_id: str, redis=Depends(get_redis)):
    recommendation = await redis.get(user_id)
    if recommendation is None:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return {"user_id": user_id, "recommendation": recommendation.decode('utf-8')}