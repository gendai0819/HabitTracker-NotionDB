import requests
import os
import dotenv
import random

dotenv.load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")

def fetch_today_data():
    url = f'https://api.notion.com/v1/databases/{DATABASE_ID}/query'

    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        entries = []

        for result in data["results"]:
            properties = result["properties"]
            word = properties["單詞"]["title"][0]["plain_text"] if properties["單詞"]["title"] else ""
            pinyin = properties["拼音"]["rich_text"][0]["plain_text"] if properties["拼音"]["rich_text"] else ""
            meaning = properties["意思"]["rich_text"][0]["plain_text"] if properties["意思"]["rich_text"] else ""

            entries.append((word, pinyin, meaning))

        # ランダムに5個選ぶ（もしデータ数が5未満でもエラーにならないようにmin）
        sample_size = min(5, len(entries))
        result_strings = []
        for word, pinyin, meaning in random.sample(entries, sample_size):
            result_strings.append(f"【単語】 {word}\n【拼音】|| {pinyin} ||\n【意味】|| {meaning} ||\n")
        return "\n".join(result_strings)
    else:
        return f"エラー: {response.status_code}, {response.text}"

if __name__ == "__main__":
    print(fetch_today_data())