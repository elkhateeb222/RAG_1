from fastapi import FastAPI
from settings import get_settings
from contextlib import asynccontextmanager
from services import VideoTranscriptor
from routes import upload_videos_router
from models import DBManager
from services import VectorDB
from routes import vector_db_router
from stores.LLM.providers import GLMProvider


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.settings=get_settings()
    app.video_transcriptor=VideoTranscriptor()
    app.db_manager = DBManager()
    app.vectorDB =VectorDB()
    app.glm = GLMProvider(
        api_key= settings.GLM_API_KEY,
        model_id=settings.GLM_MODEL_ID
        )
    yield

settings=get_settings()
app = FastAPI(
    version=settings.APP_VERSION,
    title=settings.APP_NAME,
    lifespan=lifespan
)
app.include_router(upload_videos_router)
app.include_router(vector_db_router)

    