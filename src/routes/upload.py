from services import VideoTranscriptor
from settings import get_settings
from fastapi import Request, APIRouter, UploadFile, File

from models import DBManager

from models import VideoUrlsManager


upload_videos_router = APIRouter(prefix="/upload",tags=["upload"])
video_urls=VideoUrlsManager()
db_manger=DBManager()


@upload_videos_router.post("/video_url")
async def upload_videos(request: Request, urls: list[str]):
    settings = request.app.settings
    video_transcriptor: VideoTranscriptor = request.app.video_transcriptor

    results = await video_transcriptor.parse_videos(urls)
    db_manger.index_into_table(results,urls,table_name=settings.MYSQL_VIDEOS_TABLE_NAME)

    return {"results": results}


















