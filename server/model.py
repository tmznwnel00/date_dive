from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, Date, JSON
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "User"
    
    id = Column(Integer, primary_key=True)
    age = Column(Integer)
    gender = Column(Enum('male', 'female'))
    nickname = Column(String(15))
    verified = Column(Boolean)
    created_at = Column(Date)
    updated_at = Column(Date)
    login_id = Column(String(15))
    password = Column(String)
    
class UserPhoto(Base):
    __tablename__ = "User_photo"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    s3_path = Column(String)
    photo_index = Column(Integer)
    created_at = Column(Date)
    updated_at = Column(Date)
    
class Match(Base):
    __tablename__ = "Match"
    
    id = Column(Integer, primary_key=True)
    male_id = Column(Integer)
    female_id = Column(Integer) 
    status = Column(Enum('man waiting', 'man refuse', 'woman waiting', 'woman refuse', 'matched'))
    created_at = Column(Date)
    updated_at = Column(Date)
    
class Questionnaire(Base):
    __tablename__ = "Questionnaire"
    
    id = Column(Integer, primary_key=True)
    description = Column(String)
    options = Column(JSON)
    created_at = Column(Date)
    updated_at = Column(Date)
    
class UserQuestionAnswer(Base):
    __tablename__ = "User_question_answer"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    question_id = Column(Integer)
    options_answer = Column(Integer)
    text_answer = Column(String)
    created_at = Column(Date)
    updated_at = Column(Date)
        
    
    
    