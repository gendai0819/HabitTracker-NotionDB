from NotionDB.HabitTracker import fetch_today_data
from Discord.webhook import send_to_discord

if __name__ == "__main__":
    content = fetch_today_data()
    print(content)

    if not content:
        send_to_discord("⚠️ 今日の記録は見つかりませんでした。")
    else:
        send_to_discord(content)
