from NotionDB.HabitTracker import fetch_today_data
from Discord.webhook import send_to_discord

if __name__ == "__main__":
    user_data = fetch_today_data()

    if not user_data:
        send_to_discord("⚠️ 今日の記録は見つかりませんでした。")
    else:
        for user, content in user_data.items():
            message = f"## **{user}** さんの習慣チェック\n{content}\n\n"
            message += "--------------------\n\n"
            
            send_to_discord(message)
