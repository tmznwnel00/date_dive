from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
# from model import User
import model
from database import SessionLocal, engine

from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime

model.Base.metadata.create_all(bind=engine)

# Acquired by CLI "openssl rand -hex 32"
SECRET_KEY = "9ff8f5a166924e4cc01ad9682302abf54ac778cf794cbf642074bf3ed58ccaf0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class SingupInfo(BaseModel):
    id: str
    password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username):
    return db.query(model.User).filter(model.User.login_id == username).first()
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
        db_user = model.User(login_id=username, password=hashed_password, created_at = now, updated_at = now)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    

    
    
    
    return "asfsadfsafs"