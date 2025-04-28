import requests
import os
import dotenv
dotenv.load_dotenv("../.env")


NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")


url = f'https://api.notion.com/v1/databases/{DATABASE_ID}/query'

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}
print(NOTION_TOKEN)
print(DATABASE_ID)

response = requests.post(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    for result in data["results"]:
        print(result["properties"])
else:
    print("エラー:", response.status_code, response.text)
