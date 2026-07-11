import re
from youtube_transcript_api import YouTubeTranscriptApi
from typing import List
from settings import get_settings
import asyncio
import logging
import yt_dlp
import warnings; warnings.filterwarnings("ignore")


class VideoTranscriptor:
    def __init__(self):
        self.logger = logging.getLogger("uvicorn")
        self.settings = get_settings()

    def get_video_size(self, url: str) -> int | None:
        """Returns video size in bytes (best available format), or None if unknown."""
        ydl_opts = {"quiet": True, "skip_download": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            # filesize is exact; filesize_approx is an estimate if exact isn't available
            size = info.get("filesize") or info.get("filesize_approx")
            self.logger.warning(f"video size: {size}")
            return size

    async def parse_videos(self, VDZRLs: List[str]) -> List[str]:
        results = []
        for index, url in enumerate(VDZRLs, 1):

            size = self.get_video_size(url)

            if size is None or size > self.settings.MAX_SIZE_YOUTUBE_VIDEO:
                self.logger.warning(f"faild to parse link no : {index} ")
                continue

            match = re.search(r"(?:v=|youtu\.be/|shorts/)([0-9A-Za-z_-]{11})", url)
            video_id = match.group(1) if match else url
            try:
                transcript = YouTubeTranscriptApi().fetch(video_id, languages=["ar", "en"])
                results.append(" ".join(snippet.text for snippet in transcript))
                self.logger.warning(f"succefully parsed link no : {index} ")
            except Exception as e:
                self.logger.error(f"faild to parse video no {index}: {e}")

        self.logger.warning(f"No. of parsed vides: {sum([bool(v) for v in results])}")
        return results


if __name__ == "__main__":
    video_transcriptor = VideoTranscriptor()
    content = asyncio.run(video_transcriptor.parse_videos([
        "https://youtu.be/NEbKcifBen8?si=vEU--0oaw52JRJaA",
        "https://youtu.be/-Zib7r3HxyY?si=TS7W6GZ_EXVALjWF",
        "https://youtu.be/SZ5Aznjf8Kc?si=6gczHQEVwueBJVVm"]))
    print()