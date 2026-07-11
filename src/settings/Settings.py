
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    APP_NAME:str
    APP_VERSION:str
    MAX_NUMBER_OF_YOUTUBE_URLS:int
    MAX_SIZE_YOUTUBE_VIDEO:int
    MYSQL_ROOT_PASSWORD:str
    MYSQL_DATABASE:str
    MYSQL_USER:str
    MYSQL_PASSWORD:str
    MYSQL_HOST:str


    
    
    model_config = ConfigDict(env_file='../.env')





def get_settings():
    return Settings()
    

