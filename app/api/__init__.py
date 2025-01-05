from fastapi import APIRouter, HTTPException, Depends, FastAPI, Request
from .recommendations import router as recommendations_router

router = APIRouter(prefix='/api')

router.include_router(recommendations_router)