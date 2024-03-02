from fastapi import APIRouter
from server.api.user import router as user_router
from server.api.match import router as match_router


router = APIRouter()
router.include_router(user_router, prefix='/user')
router.include_router(match_router, prefix='/match')