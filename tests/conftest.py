from fastapi.testclient import TestClient
from myapp.main import app
import pytest
#I am creating a test database
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from  myapp import models
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
from myapp.database import get_db
from myapp.router.oauth2 import jwt_token

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/fastapi_test"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()




#this fixture will run before the app starts. it will remove the tables and create new ones so that whenever we try to create an user "user already exists" issue could be avoided
@pytest.fixture #this object returns db object
def session():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture #this object returns session obj
def client(session):
   def test_db():
        try:
           yield session
        finally:
           session.close()
   app.dependency_overrides[get_db] = test_db  #this statement basically overwrites the actual db get_db with our test_db
   yield TestClient(app)

@pytest.fixture()
def test_user(client):
    user_data={
        "username":"vijay@gmail.com",
        "password":"goat"
    }
    res=client.post("/signup",data=user_data)
    output=res.json()
    output["password"]=user_data["password"]
    return output
    assert res.status_code==200

@pytest.fixture()
def test_user2(client):
    user_data={
        "username":"pranav@gmail.com",
        "password":"goat"
    }
    res=client.post("/signup",data=user_data)
    output=res.json()
    output["password"]=user_data["password"]
    return output
    assert res.status_code==200

@pytest.fixture 
def create_token(test_user):
    token=jwt_token(
        {
            "user_id":test_user["id"]
        }
    )
    return token



@pytest.fixture 
def authorized_client(client,create_token):
    #for authorised client i am altering the header by adding token
    client.headers={
        **client.headers,
        "Authorization": "Bearer {}".format(create_token)
    }
    print(client)
    return client
   
#you need a user logged in to create posts and also u need session
@pytest.fixture
def test_posts(test_user,session,test_user2):
    posts=[
        {
            "title":"title1",
            "content":"hello world",
            "user_id":test_user["id"],
            "public":True
        },
         {
            "title":"title2",
            "content":" world",
            "user_id":test_user2["id"],
            "public":True
        }
    ]

    def createPostModel(post):
        return models.Blogs(**post)

    post_map=map(createPostModel,posts)
    session.add_all(list(post_map))
    session.commit()

    all_post=session.query(models.Blogs).all()
    return all_post

