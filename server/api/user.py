from base64 import encodebytes
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from smtplib import SMTP
from typing import Union

from fastapi import Depends, HTTPException
from fastapi import APIRouter
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import HTMLResponse

from server.config import EMAIL_ADDRESS, EMAIL_PASSWORD, \
    JWT_SECRET_KEY, JWT_ALGORITHM, JWT_ACCESS_TOKEN_EXPIRE_MINUTES
from server.db import models
from server.db.base import get_db


router = APIRouter()


class SingupInfo(BaseModel):
    email: str
    password: str
    nickname: str = None
    gender: str = None
    location: str = None


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

def send_email(to_email, subject, message):
    msg = MIMEText(message)
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = subject
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

    if get_user(db, email):
        raise HTTPException(status_code=409, detail="Email exist")
    else:
        db_user = models.User(email=email, password=get_password_hash(password), nickname=nickname, gender=gender, location=location)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        verification_token = create_access_token(data={'sub': email})
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
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Mark the user as verified in the database (this should be done in a real database)
    # user = None
    user = get_user(db, email)
    if user:
        user.verified = True
        db.commit()
        db.close()
        
        return HTMLResponse(content="<h1>Email verification successful!</h1>", status_code=200)

    raise HTTPException(status_code=404, detail="User not found")

@router.post("/login", response_model=Token)
def login(user: SingupInfo, db: Session = Depends(get_db)):
    email = user.email
    password = user.password

    user = get_user(db, email)

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
    access_token_expires = timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": email}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
        }