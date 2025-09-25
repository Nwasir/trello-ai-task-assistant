import os
import requests
from dotenv import load_dotenv

# Load API credentials
load_dotenv()
api_key = os.getenv("TRELLO_API_KEY")
api_token = os.getenv("TRELLO_API_TOKEN")

if not api_key or not api_token:
    raise ValueError("❌ Missing TRELLO_API_KEY or TRELLO_API_TOKEN in .env file")

# Test request: get your Trello boards
url = f"https://api.trello.com/1/members/me/boards"
params = {
    "key": api_key,
    "token": api_token,
    "fields": "name,url"  # Get board name and link
}

response = requests.get(url, params=params)

if response.status_code == 200:
    print("✅ Trello API connected successfully!")
    boards = response.json()
    if boards:
        print("Here are your boards:")
        for b in boards:
            print(f"- {b['name']} ({b['url']})")
    else:
        print("⚠️ No boards found on your account.")
else:
    print("❌ Error:", response.status_code, response.text)
