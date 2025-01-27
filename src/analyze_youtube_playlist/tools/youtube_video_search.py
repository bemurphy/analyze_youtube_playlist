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
            doc = YoutubeLoader.from_youtube_url(
                video_url,
                # note, you might need to locally patch pytube to get this to work
                # see https://github.com/pytube/pytube/issues/2074#issuecomment-2492647027
                add_video_info=True,
            ).load()[0]

            return f"title: {doc.metadata['title']}\n\ntranscript: " + doc.page_content
        except Exception as e:
            return f"Error performing search: {str(e)}"
