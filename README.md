# Discord Notion Integration

このプロジェクトは、Notionデータベースから情報を取得し、DiscordのWebhookを使用して特定のチャンネルに送信するPythonスクリプトです。習慣トラッカーのデータを自動的にDiscordに投稿することで、チームや個人の進捗を共有できます。

## 機能

- Notion APIを使用してデータベースから情報を取得
- Discord Webhookを使用してメッセージを送信
- GitHub Actionsを使用して毎日自動的に実行

## 必要条件

- Python 3.10以上
- Notion APIトークンとデータベースID
- Discord Webhook URL

## セットアップ

1. リポジトリをクローン

   ```bash
   git clone https://github.com/your-repo/discord-notion.git
   cd discord-notion

   ```

2. 依存関係をインストール

```sh
pip install -r requirements.txt
```

3. `.env`の作成

```sh
NOTION_TOKEN="your_notion_token"
DATABASE_ID="your_database_id"
DISCORD_WEBHOOK_URL="your_discord_webhook_url"
```

4. 実行

```sh
python main.py
```

```py

import requests
import os
import dotenv
# dotenv.load_dotenv("../.env")
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
```
