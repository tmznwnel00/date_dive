from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

user = os.getenv('USER')
password = os.getenv('PASSWORD')
SQLALCHEMY_DATABASE_URL = f"mysql://{user}:{password}@localhost/datedive"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()