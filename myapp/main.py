from fastapi import FastAPI,Response,HTTPException,status,Depends,APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional,List
from random import randint
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine,SessionLocal
from sqlalchemy.orm import Session
from .database import get_db
from . import schema,utils
from .router import authentication,blog,vote
from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient
# models.Base.metadata.create_all(bind=engine)
app=FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





app.include_router(blog.router)
app.include_router(authentication.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message":"Hey guys this is Pranav testing out FastApi by developing a simple Blog API. Along with this url , add /docs to test out the CRUD operations "}
#practice
@app.get("/sqlalchemy")
def test(db:Session=Depends(get_db)):
    data=db.query(models.Blogs).all()
    return {"my_blogs":data}





