from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
from fastapi import HTTPException, Request, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from jose import jwt, JWTError
from pydantic import BaseModel
from sqlalchemy.orm import Session

from server.config import JWT_ACCESS_TOKEN_EXPIRE_MINUTES, JWT_ALGORITHM, JWT_SECRET_KEY
from server.db import models
from server.db.base import get_db
from server.utils.typeutils import JsonSerializable

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JWTPayload(BaseModel):
    sub: str  # Subject (user identifier)
    exp: int  # Expiration time
    iat: int  # Issued at
    role: Optional[List[str]] = None  # Roles, optional


def get_user(
    db: Session, *, email: Optional[str] = None, nickname: Optional[str] = None
):
    q = db.query(models.User)
    if email:
        q = q.filter(models.User.email == email)
    if nickname:
        q = q.filter(models.User.nickname == nickname)
    return q.first()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def create_jwt_token(
    data: str,
    expires_delta: timedelta = timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES),
):
    current = datetime.utcnow()
    to_encode = JWTPayload(
        sub=data,
        exp=int((current + expires_delta).timestamp()),
        iat=int(current.timestamp()),
    )
    encoded_jwt = jwt.encode(
        to_encode.model_dump(), JWT_SECRET_KEY, algorithm=JWT_ALGORITHM
    )
    return encoded_jwt


def jwt_decode(token: str) -> JWTPayload:
    return JWTPayload(
        **jwt.decode(token, key=JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    )


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[models.User]:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        print(credentials)
        if credentials:
            token = credentials.credentials
            print(token)
            payload = self.verify_jwt(token)
            if not payload:
                raise HTTPException(
                    status_code=403, detail="Invalid authorization code."
                )
            email = payload.sub
            if email:
                user = get_user(next(get_db()), email=payload.sub)
                if user:
                    return user
                else:
                    raise HTTPException(status_code=404, detail="User not found")
            else:
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, token: str):
        try:
            payload = jwt_decode(token)
            if payload and payload.exp > datetime.utcnow().timestamp():
                return payload
        except JWTError:
            pass
