import requests
import os
import dotenv
from datetime import date, datetime, timedelta, timezone


dotenv.load_dotenv("../.env")

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
    
    JST = timezone(timedelta(hours=9))  # 日本時間のタイムゾーン
    today_str = datetime.now(JST).date().isoformat()  # 日本時間で今日の日付を取得
    user_to_md = {}

    for result in data["results"]:
        props = result["properties"]
        # print(props)

        # 作成日時から日付判定
        created_time = props.get("作成日時", {}).get("created_time")
        if not created_time:
            continue
        created_date = datetime.fromisoformat(created_time.replace("Z", "+00:00")).astimezone(JST).date()
        # print(created_date, today_str)
        if created_date.isoformat() != today_str:
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
        kiai = extract_text(props.get("気合", {}))

        # Markdownフォーマットで構築
        md_parts = []
        if kiai:    md_parts.append(f"### 気合\n- {kiai}")
        if stretch: md_parts.append(f"### ストレッチ・運動\n- {stretch}")
        if coding:  md_parts.append(f"### コーディング\n- {coding}")
        if tidy:    md_parts.append(f"### 家事\n- {tidy}")
        if free:    md_parts.append(f"### 自由記入\n- {free}")

        user_to_md[username] = "\n\n".join(md_parts)

    return user_to_md

def extract_text(prop):
    if prop.get("type") == "title":
        texts = prop.get("title", [])
    else:
        texts = prop.get("rich_text", [])
    return "、".join(t.get("plain_text", "") for t in texts if t.get("plain_text", ""))

if __name__ == "__main__":
    user_md_dict = fetch_today_data()
    for user, md in user_md_dict.items():
        print(f"# {user}\n{md}\n{'-'*30}")


# import requests
# import os
# import dotenv
# dotenv.load_dotenv("../.env")


# NOTION_TOKEN = os.getenv("NOTION_TOKEN")
# DATABASE_ID = os.getenv("DATABASE_ID")


# url = f'https://api.notion.com/v1/databases/{DATABASE_ID}/query'

# headers = {
#     "Authorization": f"Bearer {NOTION_TOKEN}",
#     "Notion-Version": "2022-06-28",
#     "Content-Type": "application/json"
# }
# print(NOTION_TOKEN)
# print(DATABASE_ID)

# response = requests.post(url, headers=headers)

# if response.status_code == 200:
#     data = response.json()
#     for result in data["results"]:
#         print(result["properties"])
# else:
#     print("エラー:", response.status_code, response.text)
