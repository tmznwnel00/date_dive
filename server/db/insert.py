# File for insert dummy data in DB
from models import *
from base import SessionLocal

def insert_data(data, model):
    db=SessionLocal()
    db.add(model(**data))
    db.commit()
    db.close()
    
if __name__ == "__main__":
    insert_data({"type":"mbti", "name":"enfp"}, Hashtag)