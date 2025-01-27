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
        # 'playlist_url': 'https://www.youtube.com/playlist?list=PLp9pLaqAQbY2byWMoUz0r_FMQmNjy_cvo',
        'playlist_url': 'https://www.youtube.com/playlist?list=PLp9pLaqAQbY0DLbhgLuBJZNHBB-vW8QCk',
        'topic': 'AI Automation',
    }

    try:
        AnalyzeYoutubePlaylist().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
