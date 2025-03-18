from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

USERNAME = "lifeatsendcloud"

def get_followers():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

      # Automatically download the correct ChromeDriver
    driver = webdriver.Chrome(options=chrome_options)

    url = f"https://www.instagram.com/{USERNAME}/"
    driver.get(url)

    time.sleep(5)  # Wait for page to load

    try:
        followers_element = driver.find_element(By.XPATH, "//meta[@property='og:description']")
        followers_text = followers_element.get_attribute("content")
        followers = followers_text.split(" ")[0].replace(",", "")  # Extract number

        print(f"Followers: {followers}")

        # Save to JSON
        with open("followers.json", "w") as file:
            json.dump({"number": followers}, file)

        return followers
    except Exception as e:
        print("Could not find followers count:", e)
        return None
    finally:
        driver.quit()

get_followers()
