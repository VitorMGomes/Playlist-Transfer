from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Setup Chrome WebDriver
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriver
service = Service(executable_path="/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

def scroll_to_load_all():
    """Scrolls down to load all songs dynamically"""
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)  # Scroll down
        time.sleep(2)  # Allow new songs to load
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # Stop scrolling when no new content loads
        last_height = new_height

def scrape_spotify_playlist(spotify_url, output_csv):
    """Scrapes song titles and artists from a Spotify playlist and saves to a CSV file."""
    
    driver.get(spotify_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(5)  # Ensure the page fully loads

    scroll_to_load_all()  # Ensure all songs are visible before scraping

    # Extract all song elements
    song_elements = driver.find_elements(By.XPATH, '//div[@data-testid="tracklist-row"]')

    all_data = []
    
    for song in song_elements:
        try:
            title = song.find_element(By.XPATH, './/div[contains(@class, "standalone-ellipsis-one-line")]').text
        except:
            title = "Unknown Title"

        try:
            artist = song.find_element(By.XPATH, './/a[contains(@class, "standalone-ellipsis-one-line")]').text
        except:
            artist = "Unknown Artist"

        all_data.append({"title": title, "artist": artist})
    
    # Save to CSV
    df = pd.DataFrame(all_data)
    
    if not df.empty:
        df.to_csv(output_csv, index=False)
        print(f"✅ Successfully saved {len(df)} songs to {output_csv}")
    else:
        print("⚠️ No data scraped. Check playlist URL or page structure.")

if __name__ == "__main__":
    # Spotify Playlist URL
    playlist_url = "https://open.spotify.com/playlist/1pGWax2KHfaoEERS5AeqCM"
    
    # Output CSV file name
    output_file = "spotify_playlist.csv"

    # Run scraper
    scrape_spotify_playlist(playlist_url, output_file)
    
    driver.quit()  # Close the WebDriver
