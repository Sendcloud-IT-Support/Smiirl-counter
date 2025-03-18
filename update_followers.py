from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import json

USERNAME = "lifeatsendcloud"

def get_followers():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    service = Service("/usr/local/bin/chromedriver")  # Path to ChromeDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    url = f"https://www.instagram.com/{USERNAME}/"
    driver.get(url)

    time.sleep(5)  # Wait for page to load

    try:
        # NEW: Extract follower count from the meta tag
        meta_tag = driver.find_element(By.XPATH, "//meta[@property='og:description']")
        content = meta_tag.get_attribute("content")
        
        # Extract number of followers (format: "X followers, Y following, Z posts")
        followers = content.split(" Followers,")[0].replace(",", "")  # Remove commas for integer conversion
        
        print(f"Followers: {followers}")

        # Save to JSON
        with open("followers.json", "w") as file:
            json.dump({"followers": followers}, file)

        return followers
    except Exception as e:
        print("Could not find followers count:", e)
        return None
    finally:
        driver.quit()

get_followers()
