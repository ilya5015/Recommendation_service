from fastapi import APIRouter, HTTPException, Depends, FastAPI, Request

router = APIRouter(prefix='/api')

def get_redis(request: Request):
    return request.app.state.redis

@router.get("/")
async def create_item(redis=Depends(get_redis)):
    redis.set('key', 'value')
    return {"message": "Item saved", "key": 'key', "value": 'value'}