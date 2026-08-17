import pymysql
from settings import get_settings
from logging import getLogger
import uuid 
from langchain_text_splitters import RecursiveCharacterTextSplitter



class DBManager:
    
    def __init__(self):
        self.settings=get_settings()
        self.logger=getLogger(__name__)
        try:
            self.conn = pymysql.Connection(
            host= self.settings.MYSQL_HOST,
            user=self.settings.MYSQL_USER,
            password=self.settings.MYSQL_PASSWORD,
            
            
                )
            self.my_cursor = self.conn.cursor()

            self.create_db_if_not_exists()
            self.create_db_tables_if_not_exists()
            self.logger.info("MySQL is up")


        except Exception as e:
            self.logger.error(f"MySQL is down {e}")

    def create_db_if_not_exists(self):
        
        self.my_cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS {self.settings.MYSQL_DATABASE}"
            )
        
    def create_db_tables_if_not_exists(self):
        self.my_cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.settings.MYSQL_DATABASE}.{self.settings.MYSQL_VIDEOS_TABLE_NAME}(video_id INT PRIMARY KEY AUTO_INCREMENT, video_uuid VARCHAR(36), video_url VARCHAR(60), video_content MEDIUMTEXT);"
        )
        self.my_cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.settings.MYSQL_DATABASE}.{self.settings.MYSQL_FILES_TABLE_NAME}(file_id INT PRIMARY KEY AUTO_INCREMENT, file_uuid VARCHAR(36), file_name VARCHAR(30), file_content MEDIUMTEXT);"
        )
        self.my_cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.settings.MYSQL_DATABASE}.{self.settings.MySQL_YOUTUBE_URLS_CHUNKS_NAME}(chunk_id INT PRIMARY KEY AUTO_INCREMENT ,video_url VARCHAR(60),chunk_content VARCHAR({self.settings.MAX_CHUNK_NO_CHARS}))"
        )
    
    def index_into_table(self,data:str,urls:str,table_name:str):
        if len(data)==0:
            self.logger.error("data was sent is empty")
            return 
        
        if table_name==self.settings.MYSQL_VIDEOS_TABLE_NAME:
            for text,url in zip(data,urls):
                video_uuid=str(uuid.uuid4())
                self.my_cursor.execute(
                    f"INSERT INTO {self.settings.MYSQL_DATABASE}.{table_name} (video_uuid,video_url,video_content) VALUES (%s,%s,%s)" ,[video_uuid,url,text]
            )
                text_splitter = RecursiveCharacterTextSplitter(
                            chunk_size = self.settings.MAX_CHUNK_NO_CHARS,
                              chunk_overlap=1)
                chunks = text_splitter.split_text(text)
                for chunk in chunks:
                    self.my_cursor.execute(
                    f"INSERT INTO {self.settings.MYSQL_DATABASE}.{table_name+"_chunks"} (video_url,chunk_content) VALUES (%s,%s)" ,[url,chunk]
                    )
                
                self.conn.commit()







    def get_ids_and_chunks_content_cols(self,table_name:str):
        self.my_cursor.execute(
            f"SELECT chunk_id FROM {self.settings.MYSQL_DATABASE}.{self.settings.MySQL_YOUTUBE_URLS_CHUNKS_NAME};"

        )
        ids=self.my_cursor.fetchall()
        ids = [
            str(i[0]) 
            for i in ids
            
        ]

        self.my_cursor.execute(
            f"SELECT chunk_content FROM {self.settings.MYSQL_DATABASE}.{self.settings.MySQL_YOUTUBE_URLS_CHUNKS_NAME};"
              
        )
        chunks_content=self.my_cursor.fetchall()
        chunks_content=[
            n[0]

            for n in chunks_content
        ]
        
        return ids,chunks_content
            



    








        

        
