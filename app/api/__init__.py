from fastapi import APIRouter
from .associate_rules_router import router as associate_rules_router

router = APIRouter()
router.include_router(associate_rules_router)