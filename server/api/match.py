
from fastapi import APIRouter, Depends, Request
from server.db.models import User

from server.utils.authutils import JWTBearer


router = APIRouter()


@router.get("/new")
async def new_matches(current_user: User = Depends(JWTBearer())):
    # TODO
    return current_user