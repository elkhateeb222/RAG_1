
from fastapi import Request, APIRouter
from settings import get_settings









vector_db_router = APIRouter(prefix="/vectorDB",tags=["vectorDB"])


@vector_db_router.post("/index")
async def insert_into_collection(request:Request):
    settings = request.app.settings
    vectorDB=request.app.vectorDB
    count=await vectorDB.index_into_collection(
        table_name= settings.MySQL_YOUTUBE_URLS_CHUNKS_NAME
    )
    
    return {
        "number_of_records" : count
    }

@vector_db_router.get("/retrieve")
async def retrieve_top_chunks(request:Request,query:str):
    vectorDB=request.app.vectorDB
    result=await vectorDB.retrieve_top_chunks(
        query=query
    )
    return {
        "top_chunks":result
    }


    



    


    
