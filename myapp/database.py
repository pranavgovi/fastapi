from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import setting

SQLALCHEMY_DATABASE_URL = "postgresql://{}:{}@{}:{}/{}".format(setting.db_username,setting.db_password,setting.db_host,setting.db_port,setting.db_name)


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
# while True:
#     try:
#         conn=psycopg2.connect(host='localhost',database='myapp',user='postgres',password='postgres',cursor_factory=RealDictCursor)
#         cursor=conn.cursor()
#         print("Database connection is successfully established")
#         break
#     except Exception as error:
#         print("Database connection failed")
#         print("Error is {}".format(error))
    #cursor factory and real dict cursor will give us column names