import requests
import json
from bs4 import BeautifulSoup

INSTAGRAM_USERNAME = "lifeatsendcloud"
URL = f"https://www.ninjalitics.com/{INSTAGRAM_USERNAME}"

def get_followers():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(URL, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        follower_count = soup.find("span", class_="follower_count")  # Adjust based on Ninjalitics HTML
        if follower_count:
            return int(follower_count.text.replace(",", ""))
    
    return None

followers = get_followers()

if followers:
    with open("followers.json", "w") as f:
        json.dump({"number": followers}, f)
    print("Updated followers count:", followers)
else:
    print("Failed to get followers")
