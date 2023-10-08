from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, Date, JSON
from sqlalchemy.orm import relationship

user = 'mysql'
password = 'Abc1234!'
SQLALCHEMY_DATABASE_URL = f"mysql://{user}:{password}@localhost/datedive"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "User"
    
    id = Column(Integer, primary_key=True)
    age = Column(Integer)
    gender = Column(Enum('male', 'female'))
    nickname = Column(String(15))
    verified = Column(Boolean)
    signup_date = Column(Date)
    
class User_photo(Base):
    __tablename__ = "User_photo"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    s3_path = Column(String)
    photo_index = Column(Integer)
    createdAt = Column(Date)
    updatedAt = Column(Date)
    
class Match(Base):
    __tablename__ = "Match_table"
    
    id = Column(Integer, primary_key=True)
    male_id = Column(Integer)
    female_id = Column(Integer) 
    status = Column(Enum('man waiting', 'man refuse', 'woman waiting', 'woman refuse', 'matched'))
    createdAt = Column(Date)
    updatedAt = Column(Date)
    
class Questionnaire(Base):
    __tablename__ = "Questionnaire"
    
    id = Column(Integer, primary_key=True)
    description = Column(String)
    options = Column(JSON)
    createdAt = Column(Date)
    updatedAt = Column(Date)
    
class User_question_answer(Base):
    __tablename__ = "User_question_answer"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    question_id = Column(Integer)
    options_answer = Column(Integer)
    text_answer = Column(String)
    createdAt = Column(Date)
    updatedAt = Column(Date)
        
    
    
    