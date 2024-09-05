from pydantic import BaseModel,EmailStr
from typing import Optional
class postInput(BaseModel):
    title:str
    content:str
    public:bool
#you are just defining your own model/schema to typehint

class credentials(BaseModel):
    email:EmailStr
    id:int
   
    


class Response(BaseModel):
    title:str
    blog_id:int
    user_id:Optional[int]
    public:Optional[bool]
    votes:Optional[int]
    owner:credentials

    class Config:
        orm_mode=True



class signresponse(BaseModel):
    user_id:int
    
    
    class Config:
        orm_mode=True

class voteinput(BaseModel):
    post_id:int
    dir:bool