from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
# from model import User
from db import models
from db.base import engine, get_db
from typing import Union

from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta


models.Base.metadata.create_all(bind=engine)

# Acquired by CLI "openssl rand -hex 32"
SECRET_KEY = "9ff8f5a166924e4cc01ad9682302abf54ac778cf794cbf642074bf3ed58ccaf0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class SingupInfo(BaseModel):
    id: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username):
    return db.query(models.User).filter(models.User.login_id == username).first()


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.get("/")
def root():
    return "start"


@app.post("/api/user/signup")
def signup(user: SingupInfo, db: Session = Depends(get_db)):
    print(user)
    username = user.id
    password = user.password

    if get_user(db, username):
        raise HTTPException(status_code=409, detail="Username exist")
    else:
        hashed_password = get_password_hash(password)
        now = datetime.now()
        db_user = models.User(login_id=username, password=hashed_password, created_at = now, updated_at = now)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user


@app.post("/api/user/login")
def login(user: SingupInfo, db: Session = Depends(get_db)):
    username = user.id
    password = user.password

    user = get_user(db, username)

    if (user == None or verify_password(password, user.password) == False):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
