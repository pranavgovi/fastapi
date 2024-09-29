


from fastapi import FastAPI,Response,HTTPException,status,Depends,APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional,List
from random import randint
import psycopg2
from psycopg2.extras import RealDictCursor

from . import oauth2
from .. import models,schema,utils
from ..database import engine,SessionLocal
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
router=APIRouter(
    tags=["UserAuthentication"]
)


#for authentication
@router.post("/signup")
def signup(db:Session=Depends(get_db),userinfo:OAuth2PasswordRequestForm=Depends()):
    if db.query(models.Authentication).filter(models.Authentication.email==userinfo.username).first():
        return "This email already has an account"
    entry=models.Authentication(email=userinfo.username,password=utils.hash(userinfo.password))
    
    db.add(entry)

    db.commit()
    db.refresh(entry)
    return entry

@router.post("/login",response_model=dict)
def login(db:Session=Depends(get_db),userinfo:OAuth2PasswordRequestForm=Depends()):
    query=db.query(models.Authentication).filter(models.Authentication.email==userinfo.username)
    db_data=query.first()
    if not userinfo.username:
        #empty username
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                            detail="Empty credentials")
    if not userinfo.password:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
                            detail="Empty credentials")

    if not db_data:
        #if the user does not exist, raise 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Username does not exist")
    #if the password is wrong return 401
    if not utils.check(userinfo.password,db_data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Invalid password")
    print("user who logged in now is:",db_data.id)
    db.commit()
    db.refresh(db_data)

    # return "Successful login for  {}".format(data.email)
    #after successful login return the access token
    token=oauth2.jwt_token(data={"user_id":db_data.id})
    return {
        "access_token":token,
        "token_type":"bearer"
    }
