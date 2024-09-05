from .database import Base
from sqlalchemy import Column,Integer,String,TIMESTAMP,text,ForeignKey,Boolean
from sqlalchemy.orm import relationship

class Blogs(Base):
    __tablename__="blogs"
    blog_id=Column(type_=Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey("authentication.id",ondelete='Cascade'))
    title=Column(type_=String,nullable=False)
    content=Column(type_=String,nullable=False)
    time=Column(type_=TIMESTAMP,nullable=False,server_default=text("CURRENT_TIMESTAMP"))
    votes=Column(type_=Integer,nullable=False,default=0)
    public=Column(Boolean,nullable=False)
    owner=relationship("Authentication")

class Authentication(Base):
    __tablename__="authentication"
    id=Column(type_=Integer,primary_key=True)
    email=Column(type_=String,unique=True,nullable=False)
    password=Column(type_=String,nullable=False)
    phonenumber=Column(type_=String,default='')
    
    
class Voting(Base):
    __tablename__="votes"
    post_id=Column(Integer,ForeignKey("blogs.blog_id",ondelete='Cascade'),primary_key=True)
    user_id=Column(Integer,ForeignKey("authentication.id",ondelete='Cascade'),primary_key=True)



    