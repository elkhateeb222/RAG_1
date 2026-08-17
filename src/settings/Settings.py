
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
    MYSQL_VIDEOS_TABLE_NAME:str
    MYSQL_FILES_TABLE_NAME:str
    MySQL_YOUTUBE_URLS_CHUNKS_NAME:str

    
    MAX_CHUNK_NO_CHARS:int


    
    
    model_config = ConfigDict(env_file='../.env')





def get_settings():
    return Settings()
    

