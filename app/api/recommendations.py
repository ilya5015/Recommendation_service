from fastapi import APIRouter, HTTPException, Depends, FastAPI, Request

router = APIRouter(prefix='/recommendations')

def get_redis(request: Request):
    return request.app.state.redis

@router.get("/get_recommendations")
async def get_recommendation(user_id:int, redis=Depends(get_redis)):
    print('fdsfdsfsdf', redis)
    recommendations = redis.get(user_id)
    if recommendations is None:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return {"user_id": user_id, "recommendations": recommendations}