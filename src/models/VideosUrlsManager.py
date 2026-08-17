import pymysql
from settings import get_settings
from logging import getLogger




class VideoUrlsManager:
    
    def __init__(self):
        self.logger=getLogger(__name__)

        self.settings=get_settings()
        ...



        
    