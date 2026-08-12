import requests
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = "@migajasrandom"
OFFSET_FILE = "telegram_offset.txt"

offset = 0
if os.path.exists(OFFSET_FILE):
    with open(OFFSET_FILE) as f:
        content = f.read().strip()
        if content:
            offset = int(content)

url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
params = {"offset": offset, "timeout": 0}
resp = requests.get(url, params=params).json()

max_update_id = offset - 1 if offset else 0

for update in resp.get("result", []):
    max_update_id = update["update_id"]
    message = update.get("message", {})
    new_members = message.get("new_chat_members")
    if new_members:
        for member in new_members:
            if member.get("is_bot"):
                continue
            first_name = member.get("first_name", "")
            user_id = member["id"]
            mention = f'<a href="tg://user?id={user_id}">{first_name}</a>'
            text = f"¡Bienvenido/a al grupo, {mention}! 🎉"
            send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            payload = {
                "chat_id": CHAT_ID,
                "text": text,
                "parse_mode": "HTML"
            }
            requests.post(send_url, json=payload)
            print(f"Bienvenida enviada a {first_name}")

if resp.get("result"):
    with open(OFFSET_FILE, "w") as f:
        f.write(str(max_update_id + 1))
else:
    print("Sin novedades")
