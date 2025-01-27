#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from analyze_youtube_playlist.crew import AnalyzeYoutubePlaylist

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'bullet_point_count': 10,
        # 'playlist_url': 'https://www.youtube.com/playlist?list=PLp9pLaqAQbY2byWMoUz0r_FMQmNjy_cvo',
        'playlist_url': 'https://www.youtube.com/playlist?list=PLp9pLaqAQbY0DLbhgLuBJZNHBB-vW8QCk',
        # 'playlist_url': 'https://www.youtube.com/playlist?list=PLR9VGbemPA587TEYarnENQ34Gb49HgL_X',
        # 'playlist_url': 'https://www.youtube.com/playlist?list=PLR9VGbemPA58hRXZFls4qWisLhDig_-H2',
        # 'bullet_point_count': 4,
    }

    try:
        AnalyzeYoutubePlaylist().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
