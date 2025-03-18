import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import json

USERNAME = "lifeatsendcloud"

def get_followers():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("window-size=1920,1080")  # Ensure full page loads

    # Use different ChromeDriver paths based on the environment
    driver_path = "chromedriver.exe" if os.name == "nt" else "/usr/bin/chromedriver"
    service = Service(driver_path)

    driver = webdriver.Chrome(service=service, options=chrome_options)

    url = f"https://www.instagram.com/{USERNAME}/"
    driver.get(url)

    try:
        time.sleep(5)  # Wait for the page to load

        # ✅ Accept Cookies if present
        try:
            accept_cookies_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept all')]"))
            )
            accept_cookies_button.click()
            print("✅ Accepted Cookies")
        except Exception:
            print("⚠️ No cookie popup found, continuing...")

        # ✅ Locate the meta description
        followers_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//meta[@property='og:description']"))
        )
        followers_text = followers_element.get_attribute("content")

        # 🔹 Use REGEX to extract only the number of followers
        match = re.search(r"(\d{1,3}(?:,\d{3})*) followers", followers_text)
        if match:
            followers = match.group(1).replace(",", "")  # Remove commas for proper number format
            print(f"👥 Followers: {followers}")

            # Save followers count to JSON
            with open("followers.json", "w") as file:
                json.dump({"number": int(followers)}, file)

            return followers
        else:
            raise ValueError(f"Could not extract followers count from: {followers_text}")

    except Exception as e:
        print("❌ Could not find followers count:", e)
        return None

    finally:
        driver.quit()

get_followers()
