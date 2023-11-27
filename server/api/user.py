from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, HTTPException
from fastapi import APIRouter
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from server.config import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_ACCESS_TOKEN_EXPIRE_MINUTES
from server.db import models
from server.db.base import get_db


router = APIRouter()


class SingupInfo(BaseModel):
    email: str
    password: str
    nickname: str
    gender: str
    location: str


class Token(BaseModel):
    access_token: str
    token_type: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, email):
    return db.query(models.User).filter(models.User.email == email).first()


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


@router.post("/signup")
def signup(user: SingupInfo, db: Session = Depends(get_db)):
    email = user.email
    password = user.password
    nickname = user.nickname
    gender = user.gender
    location = user.location

    if get_user(db, email):
        raise HTTPException(status_code=409, detail="Email exist")
    else:
        db_user = models.User(email=email, password=get_password_hash(password), nickname=nickname, gender=gender, location=location)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user


@router.post("/login", response_model=Token)
def login(user: SingupInfo, db: Session = Depends(get_db)):
    email = user.email
    password = user.password

    user = get_user(db, email)

    if (user == None or verify_password(password, user.password) == False):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        access_token_expires = timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": email}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
