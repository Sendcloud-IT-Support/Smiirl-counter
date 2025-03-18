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
    # options.add_argument("--headless")  # Uncomment this for GitHub Actions
    options.add_argument("window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")

    driver = uc.Chrome(options=options)
    driver.get(f"https://www.instagram.com/{USERNAME}/")

    try:
        time.sleep(10)  # Increased sleep time for better reliability

        # First try the og:description method
        try:
            followers_element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//meta[@property='og:description']"))
            )
            followers_text = followers_element.get_attribute("content")
            followers = followers_text.split()[0].replace(",", "")
        except:
            print("⚠️ og:description not found, trying an alternative method...")

            # Alternative method: Look for followers directly on the page
            followers_element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'followers')]/preceding-sibling::span"))
            )
            followers = followers_element.text.replace(",", "")

        print(f"👥 Followers: {followers}")
        return followers

    except Exception as e:
        print("❌ Could not find followers count:", e)
        return None

    finally:
        try:
            driver.quit()
        except Exception as e:
            print("⚠️ Error closing WebDriver:", e)
        del driver  # Ensure cleanup

# Run the function
get_followers()

# Force a clean exit
sys.exit(0)
