import sys
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

USERNAME = "lifeatsendcloud"

def get_followers():
    options = uc.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("window-size=1920,1080")

    driver = uc.Chrome(options=options)
    driver.get(f"https://www.instagram.com/{USERNAME}/")

    try:
        time.sleep(5)  # Wait for content to load

        followers_element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//meta[@property='og:description']"))
        )

        followers_text = followers_element.get_attribute("content")
        followers = followers_text.split()[0].replace(",", "")

        print(f"👥 Followers: {followers}")
        return followers

    except Exception as e:
        print("❌ Could not find followers count:", e)
        return None

    finally:
        if driver:
            driver.quit()
        del driver  # Ensure cleanup

# Run the function
get_followers()

# Force a clean exit
sys.exit(0)
