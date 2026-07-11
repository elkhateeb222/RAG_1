from services import VideoTranscriptor
from settings import get_settings
from fastapi import Request, APIRouter, UploadFile, File

from models import VideoUrlsManager


upload_videos_router = APIRouter()
video_urls=VideoUrlsManager()


@upload_videos_router.post("/upload/video")
async def upload_videos(request: Request, urls: list[str]):
    settings = request.app.settings
    video_transcriptor: VideoTranscriptor = request.app.video_transcriptor

    results = await video_transcriptor.parse_videos(urls)

    return {"results": results}


@upload_videos_router.post("/upload/file")
async def upload_file(file: UploadFile = File(...)):
    """
    Accepts a file upload, saves it locally, and returns metadata.
    """
    return await upload_video(file)















