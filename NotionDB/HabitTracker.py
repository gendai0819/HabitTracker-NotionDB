import requests
import os
import dotenv
from datetime import date

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
    if response.status_code != 200:
        print("エラー:", response.status_code, response.text)
        return {}

    data = response.json()
    today_str = date.today().isoformat()
    user_to_md = {}

    for result in data["results"]:
        props = result["properties"]

        # 日付判定（Dayが@今日 or 今日の日付）
        day_prop = props.get("Day", {}).get("title", [])
        if not day_prop:
            continue
        day_text = "".join(part.get("plain_text", "") for part in day_prop)
        if today_str not in day_text and "@今日" not in day_text:
            continue

        # ユーザー名の取得
        people = props.get("ユーザー", {}).get("people", [])
        if not people:
            continue
        username = people[0].get("name", "Unknown")

        # 各項目を抽出
        stretch = extract_text(props.get("stretch-workout", {}))
        coding = extract_text(props.get("coding", {}))
        tidy = extract_text(props.get("Tidy家事", {}))
        free = extract_text(props.get("free", {}))

        # Markdownフォーマットで構築
        md_parts = []
        if stretch: md_parts.append(f"### ストレッチ・運動\n- {stretch}")
        if coding:  md_parts.append(f"### コーディング\n- {coding}")
        if tidy:    md_parts.append(f"### 家事\n- {tidy}")
        if free:    md_parts.append(f"### 自由記入\n- {free}")

        user_to_md[username] = "\n\n".join(md_parts)

    return user_to_md

def extract_text(prop):
    texts = prop.get("rich_text", [])
    return "、".join(t.get("plain_text", "") for t in texts if t.get("plain_text", ""))


if __name__ == "__main__":
    user_md_dict = fetch_today_data()
    for user, md in user_md_dict.items():
        print(f"# {user}\n{md}\n{'-'*30}")
