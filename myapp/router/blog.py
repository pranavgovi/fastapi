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
    tags=['BlogPosts']
)
#working
@router.get("/posts",response_model=List[schema.Response])
def sendPost(search:Optional[str]="",db:Session=Depends(get_db),user_id=Depends(oauth2.getCurrentUser),limit:int=10,skip:int=0):
    posts=db.query(models.Blogs).filter(
        or_(
            models.Blogs.user_id==user_id,
            models.Blogs.public
        )
    ).filter(models.Blogs.title.contains(search)).limit(limit).offset(skip).all()
    # votes_dict={}
    # votes=db.query(models.Voting.post_id).all()
    # posts_votes=[i[0] for i in votes]
    # for i in posts_votes:
    #     if i not in votes_dict:
    #         votes_dict[i]=1
    #     else:
    #         votes_dict[i]+=1
    


    # query=""" select * from posts """
    # cursor.execute(query)
    # posts=cursor.fetchall()
  
    return posts


#by including a dependency function for creating a post, everytime when a user tries to create a post , under oauth file getcurrent user function is called that inturn checks whether the token is present is the header and it is valid or not
@router.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schema.Response)
def create_post(output:schema.postInput=Body(...),db:Session=Depends(get_db),user_id=Depends(oauth2.getCurrentUser)):
    entry=models.Blogs(title=output.title,content=output.content,user_id=user_id,public=output.public)
    
    
    db.add(entry)
    db.commit()
    

    db.refresh(entry) #to return the post to the client/postman similar to returning *
    # output=output.dict()
    # query=""" insert into posts(title ,contents) values (%s,%s) returning * """
    # cursor.execute(query,(output["title"],output["content"]))
    # post=cursor.fetchone()
    # conn.commit()
    return entry






@router.get("/posts/{id}",response_model=schema.Response)
def getPosts(id:int,response:Response,db:Session=Depends(get_db),user_id=Depends(oauth2.getCurrentUser)):    # query=""" select * from posts where id=(%s) """
    # #you dont have to add returning for select as it will autmatically display..insert update delete only requires returing statement
    # cursor.execute(query,(id,))
    # post=cursor.fetchone()
    # conn.commit()

    post=db.query(models.Blogs).filter(models.Blogs.blog_id==id).first()
    db.commit()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"No records found for this {id} id")
    if post.user_id!=user_id and post.public!=True:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail=f"This post is private")
    return post
    
#working    
@router.delete("/posts/{id}")
def deletePost(id:int,db:Session=Depends(get_db),user_id=Depends(oauth2.getCurrentUser)):
    # query="""delete from posts where id=(%s) returning *"""
    # cursor.execute(query,(id,))
    # post=cursor.fetchone()
    # conn.commit()
    post=db.query(models.Blogs).filter(models.Blogs.blog_id==id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No records found for this {} id".format(id))
    if post.user_id!=user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You cant access this".format(id))
    db.delete(post)
    db.commit()
    return "successfully deleted"
    

#working
@router.put("/posts/{id}",response_model=schema.Response)
def update_post(id:int,updatedcontent:schema.postInput=Body(...),db:Session=Depends(get_db),user_id=Depends(oauth2.getCurrentUser)):
    # query="""update posts set title=(%s) , contents=(%s) where id=(%s) returning *"""
    # cursor.execute(query,(updatedcontent.title,updatedcontent.content,id))
    # updatedpost=cursor.fetchone()
    # conn.commit()
    # post_query=db.query(models.Blogs).filter(models.Blogs.id==id)
    # post=post_query.first()
    # post_query.update(updatedcontent.dict(),synchronize_session=False)
    post=db.query(models.Blogs).filter(models.Blogs.blog_id==id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No records found for this {} id".format(id))
    if post.user_id!=user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You cant access this".format(id))
    post.title=updatedcontent.title
    post.content=updatedcontent.content
    db.commit()
    db.refresh(post)

    return post


    
