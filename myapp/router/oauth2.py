from jose import JWTError, jwt
from datetime import datetime,timedelta,timezone
from fastapi.security import OAuth2PasswordBearer
from .. import schema,models
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException,status
from ..config import setting

oauthscheme=OAuth2PasswordBearer(tokenUrl='login')


ALGORITHM=setting.algorithm
SECRET_KEY=setting.secret_key
def jwt_token(data:dict):
    new_data=data.copy()
    # I am copying the dict so that the original data is not modified
    expiration = datetime.now(timezone.utc) + timedelta(minutes=setting.expire)
    #here 30 minutes denotes that the token is gonna expire from 30 mins now on
    new_data.update({"exp":expiration.timestamp()})
    encoded_jwt=jwt.encode(new_data,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def validate_token(token:str,output_exception):
    #logic for validating token
    try:
        data=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM]) #here algorithm is in plural so pass an array
        user_id:int=data.get("user_id")
        if not user_id:
            raise output_exception
    except JWTError:
        # Handle all JWT errors, including expiration
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return schema.signresponse(user_id=user_id)

def getCurrentUser(token:str=Depends(oauthscheme),db:Session=Depends(get_db)):
    #I got the token from header using this oauthscheme . As you see when the user hits the endpoint login , Fastapi is instructed to obtain the token from header
    output_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Invalid credentials", headers={"WWW-Authenticate": "Bearer"})
    sign_response=validate_token(token,output_exception)
    user_data=db.query(models.Authentication).filter(models.Authentication.id==sign_response.user_id).first()
    return user_data.id