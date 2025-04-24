import os
import dotenv
import requests

dotenv.load_dotenv()
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_to_discord(content: str):
    if not WEBHOOK_URL:
        raise ValueError("DISCORD_WEBHOOK_URLが.envに設定されていません。")

    data = {
        "content": content
    }

    response = requests.post(WEBHOOK_URL, json=data)
    if response.status_code != 204:
        print("送信失敗:", response.status_code, response.text)
    else:
        print("✅ Discordに送信しました")

if __name__ == "__main__":
    # テスト用のメッセージを送信
    test_message = "これはテストメッセージです。"
    send_to_discord(test_message)