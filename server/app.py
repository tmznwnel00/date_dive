# from model import User
from fastapi import FastAPI

from server.db import models
from server.db.base import engine
from server import api

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return "start"


app.include_router(api.router, prefix='/api')