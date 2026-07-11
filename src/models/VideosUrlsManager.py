import pymysql
from settings import get_settings
from logging import getLogger




class VideoUrlsManager:
    
    def __init__(self):
        self.logger=getLogger(__name__)

        self.settings=get_settings()


        self.conn = pymysql.Connection(


           host= self.settings.MYSQL_HOST,
           user=self.settings.MYSQL_USER,
           password=self.settings.MYSQL_PASSWORD,
           database=self.settings.MYSQL_DATABASE,



            
        )
        self.logger.info("mysql connection")




        
    