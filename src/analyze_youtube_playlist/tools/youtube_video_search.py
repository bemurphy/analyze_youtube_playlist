from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from langchain_community.document_loaders import YoutubeLoader

class YoutubeVideoSearch(BaseTool):
    name: str = "YouTube Video Search"
    description: str = (
        "Search youtube for a video transcript given a video url"
    )

    def _run(self, video_url: str) -> str:
        # print('!!! DEBUG !!!')
        # print(video_url)
        # print('!!! DEBUG !!!')

        try:
            return YoutubeLoader.from_youtube_url(
                video_url,
                add_video_info=False,
            ).load()[0].page_content
        except Exception as e:
            return f"Error performing search: {str(e)}"
