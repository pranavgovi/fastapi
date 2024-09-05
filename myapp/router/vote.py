from fastapi import FastAPI,Response,HTTPException,status,Depends,APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional,List
from random import randint
import psycopg2
from psycopg2.extras import RealDictCursor
from .. import models
from ..database import engine,SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..database import get_db
from .. import schema
from . import oauth2
router=APIRouter(
    tags=['Vote']
)
#working
@router.post("/vote")
def vote(db:Session=Depends(get_db),user_id=Depends(oauth2.getCurrentUser),voteinput:schema.voteinput=Body(...)):
    #user will send you a post id and his vote
    #first check if there is any post of tht id
    query=db.query(models.Blogs).filter(models.Blogs.blog_id==voteinput.post_id)
    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No post found for this id")
    postquery=db.query(models.Voting).filter(models.Voting.post_id==voteinput.post_id,models.Voting.user_id==user_id)
    if voteinput.dir==1:
        #check if there is a vote already by this user
    
        if not postquery.first():

            db.add(models.Voting(post_id=voteinput.post_id,user_id=user_id))
            db.commit()
            post=db.query(models.Blogs).filter(models.Blogs.blog_id==voteinput.post_id).first()
            if post.votes:
                prev_votes=int(post.votes)
            else:
                prev_votes=0
            

            update_post=db.query(models.Blogs).filter(models.Blogs.blog_id==voteinput.post_id).first()
            update_post.votes=prev_votes+1
            db.commit()
            
            return "Voted successfully"
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="already liked")
    else:
        #delete the entry from the database
        if not postquery.first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="there is no like only")
        else:
            db.delete(postquery.first())
            db.commit()
            post=db.query(models.Blogs).filter(models.Blogs.blog_id==voteinput.post_id).first()
            if post.votes:
                prev_votes=int(post.votes)
          
            

            update_post=db.query(models.Blogs).filter(models.Blogs.blog_id==voteinput.post_id).first()
            update_post.votes=prev_votes-1
            db.commit()
            
            return "Vote deleted successfully"
            


    