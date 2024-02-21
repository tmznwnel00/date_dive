from base64 import encodebytes
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from smtplib import SMTP
from typing import Optional, Union

from fastapi import Depends, HTTPException
from fastapi import APIRouter
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import HTMLResponse

from server.config import (
    EMAIL_ADDRESS,
    EMAIL_PASSWORD,
    JWT_SECRET_KEY,
    JWT_ALGORITHM,
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
)
from server.db import models
from server.db.base import get_db
from server.utils.authutils import (
    create_jwt_token,
    get_password_hash,
    jwt_decode,
    verify_password,
)


router = APIRouter()


class SigninInfo(BaseModel):
    email: str
    password: str


class SingupInfo(SigninInfo):
    nickname: str = None
    gender: str = None
    location: str = None


class Token(BaseModel):
    access_token: str
    token_type: str


def get_user(db, *, email: Optional[str] = None, nickname: Optional[str] = None):
    q = db.query(models.User)
    if email:
        q = q.filter(models.User.email == email)
    if nickname:
        q = q.filter(models.User.nickname == nickname)
    return q.first()


def send_email(to_email, subject, message):
    msg = MIMEText(message)
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject
    with SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        server.quit()


def send_verification_email(to_email, token):
    subject = "Verify Your Email"
    message = f"Click the following link to verify your email: http://127.0.0.1:8000/api/user/verify?token={token}"
    send_email(to_email, subject, message)


@router.post("/signup")
def signup(user: SingupInfo, db: Session = Depends(get_db)):
    email = user.email
    password = user.password
    nickname = user.nickname
    gender = user.gender
    location = user.location

    if get_user(db, email=email):
        raise HTTPException(status_code=409, detail="This email can not be used")
    if get_user(db, nickname=nickname):
        raise HTTPException(status_code=409, detail="Nickname exists")
    else:
        db_user = models.User(
            email=email,
            password=get_password_hash(password),
            nickname=nickname,
            gender=gender,
            location=location,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        verification_token = create_jwt_token(email)
        send_verification_email(email, verification_token)

        return db_user


@router.get("/verify")
async def verify_email(token: str, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the token to get the email
        payload = jwt_decode(token)
        email: str = payload.sub
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Mark the user as verified in the database (this should be done in a real database)
    # user = None
    user = get_user(db, email=email)
    if user:
        user.verified = True
        db.commit()
        db.close()

        return HTMLResponse(
            content="<h1>Email verification successful!</h1>", status_code=200
        )

    raise HTTPException(status_code=404, detail="User not found")


@router.post("/login", response_model=Token)
def login(user: SigninInfo, db: Session = Depends(get_db)):
    email = user.email
    password = user.password

    user = get_user(db, email=email)

    if user == None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Verify email address",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_jwt_token(email)
    return Token(access_token=access_token, token_type="bearer")
