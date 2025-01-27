from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

def scrape_youtube_playlist(playlist_url):
    # Set up Selenium WebDriver with headless Chrome
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
            video_data.append({
                "title": title_element.text.strip(),
                "url": title_element.get_attribute("href")
            })

        # Return scraped data
        return video_data
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        # Quit the driver
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <playlist_url>", file=sys.stderr)
        sys.exit(1)

    playlist_url = sys.argv[1].strip()
    if not playlist_url.startswith("http"):
        print("Please provide a valid URL", file=sys.stderr)
        sys.exit(1)

    data = scrape_youtube_playlist(playlist_url)
    for video in data:
        print(video["url"])

