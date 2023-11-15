# from model import User
from fastapi import FastAPI

from db import models
from db.base import engine
import api

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return "start"


app.include_router(api.router, prefix='/api')