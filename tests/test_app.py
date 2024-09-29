from .conftest import client,session
import pytest
from myapp.router.oauth2 import getCurrentUser
from jose import jwt
from myapp.config import setting

def test_app(client):
    res=client.get("/") #response
    assert res.status_code ==200
    assert res.json().get("message")== "Hey guys this is Pranav testing out FastApi by developing a simple Blog API. Along with this url , add /docs to test out the CRUD operations "





def test_login(test_user,client):
    res=client.post("/login",data={
        "username":test_user["email"],
        "password":test_user["password"]
    })
    data=res.json()
    access_token=data["access_token"]
    assert res.status_code==200
    assert data['token_type'] == 'bearer'
    
    data=jwt.decode(access_token,setting.secret_key,algorithms=[setting.algorithm]) #here algorithm is in plural so pass an array
    user_id:int=data.get("user_id")
    assert user_id==data["user_id"]

@pytest.mark.parametrize("email,password,status_code",[("vijay@gmail.com","got",401),("vinay@gmail.com","got",404),
(None,"goat",422),
("vay@gmail.com",None,422)

])
#always for missing data return 422
#if the credentials are wrong return 401, if there is no such username return 404
def test_incorrectlogin(test_user,client,email,password,status_code):

     #for testing purpose i add an user to db and check the incorrect login tests
    res=client.post("/login",data={
        "username":email,
        "password":password
    })

    assert res.status_code==status_code
    