from fastapi import APIRouter
from server.api.user import router as user_router


router = APIRouter()
router.include_router(user_router, prefix='/user')