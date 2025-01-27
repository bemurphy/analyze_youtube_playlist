from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys

class YoutubePlaylistScraperInput(BaseModel):
    """Input schema for YoutubePlaylistScraper."""
    playlist_url: str = Field(..., description="The URL of the YouTube playlist to scrape.")

class YoutubePlaylistScraper(BaseTool):
    name: str = "Youtube Playlist Scraper"
    description: str = (
        "A tool for scraping and analyzing YouTube playlists to extract video information."
    )
    args_schema: Type[BaseModel] = YoutubePlaylistScraperInput

    def _run(self, playlist_url: str) -> str:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")  # Recommended for headless
        chrome_options.add_argument("--no-sandbox")  # Useful for some environments
        chrome_options.add_argument("--disable-dev-shm-usage")  # Avoid shared memory issues

        driver = webdriver.Chrome(options=chrome_options)

        try:
            # Open the playlist URL
            driver.get(playlist_url)

            # Wait for the page to load
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-playlist-video-list-renderer")))

            # Scrape video titles and URLs
            videos = driver.find_elements(By.CSS_SELECTOR, "ytd-playlist-video-renderer")
            video_data = []
            for video in videos:
                title_element = video.find_element(By.CSS_SELECTOR, "#video-title")
                video_data.append(title_element.get_attribute("href"))

            # Truncate video list to max videos for now for dev speed
            video_data = video_data[:6]

            # Return scraped data as string with newlines
            return "\n".join(video_data)
        except Exception as e:
            print(f"Error: {e}")
            return []
        finally:
            # Quit the driver
            driver.quit()