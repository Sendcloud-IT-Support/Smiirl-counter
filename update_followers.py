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

    # Use installed ChromeDriver
    service = Service("/usr/bin/chromedriver")  
    driver = webdriver.Chrome(service=service, options=chrome_options)

    url = f"https://www.instagram.com/{USERNAME}/"
    driver.get(url)

    time.sleep(5)  # Wait for page to load

    try:
        followers_element = driver.find_element(By.XPATH, "//span[contains(@class, 'x1lliihq')]")
        followers = followers_element.text
        print(f"Followers: {followers}")

        # Save to JSON
        with open("followers.json", "w") as file:
            file.write(f'{{"number": {followers}}}')

        return followers
    except Exception as e:
        print("Could not find followers count:", e)
        return None
    finally:
        driver.quit()

get_followers()
