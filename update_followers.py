from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

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
        time.sleep(5)  # Wait for dynamic content

        # Use a more reliable XPath to locate the followers count
        followers_element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//meta[@property='og:description']"))
        )

        followers = followers_element.text.replace(",", "").split()[0]
        print(f"Followers: {followers}")

        # Save followers count
        with open("followers.json", "w") as file:
            file.write(f'{{"number": {followers}}}')

        return followers
    except Exception as e:
        print("Could not find followers count:", e)
        return None
    finally:
        driver.quit()

get_followers()
