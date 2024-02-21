from datetime import datetime, timedelta
import json
from typing import Dict, List, Optional, Union
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from jose import jwt, JWTError
from pydantic import BaseModel

from server.config import JWT_ACCESS_TOKEN_EXPIRE_MINUTES, JWT_ALGORITHM, JWT_SECRET_KEY
from server.utils.typeutils import JsonSerializable

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JWTPayload(BaseModel):
    sub: str  # Subject (user identifier)
    exp: int  # Expiration time
    iat: int  # Issued at
    role: Optional[List[str]] = None  # Roles, optional


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def create_jwt_token(
    data: JsonSerializable,
    expires_delta: timedelta = timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES),
):
    current = datetime.utcnow()
    to_encode = JWTPayload(
        sub=json.dumps(data), iat=current, exp=current + expires_delta
    )
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def jwt_decode(token: str) -> JWTPayload:
    return JWTPayload(
        **jwt.decode(token, key=JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    )