from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

USERNAME = "lifeatsendcloud"

def get_followers():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    # Remove --headless for debugging
    # chrome_options.add_argument("--headless")

    service = Service("chromedriver.exe")  # Path to chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)

    url = f"https://www.instagram.com/{USERNAME}/"
    driver.get(url)

    try:
        followers_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//meta[@property='og:description']"))
        )
        followers_text = followers_element.get_attribute("content")
        followers = followers_text.split(" Followers")[0].replace(",", "")
        
        print(f"Followers: {followers}")
        return followers
    except Exception as e:
        print("Could not find followers count:", e)
        return None
    finally:
        driver.quit()

followers = get_followers()
