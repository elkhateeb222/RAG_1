from fastapi import FastAPI
from settings import get_settings
from contextlib import asynccontextmanager
from services import VideoTranscriptor
from routes import upload_videos_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    app.settings=get_settings()
    app.video_transcriptor=VideoTranscriptor()
    yield

settings=get_settings()
app = FastAPI(
    version=settings.APP_VERSION,
    title=settings.APP_NAME,
    lifespan=lifespan
)
app.include_router(upload_videos_router)

    