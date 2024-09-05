from pydantic_settings import BaseSettings
class Setting(BaseSettings):
    db_host:str=''
    db_port:str=''
    db_password:str=''
    db_name:str=''
    db_username:str=''
    secret_key:str=''
    algorithm:str=""
    expire:int =0

    class Config:
        env_file=".env"
setting=Setting()

