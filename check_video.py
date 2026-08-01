import requests
import os

API_KEY = os.environ["YT_API_KEY"]
CHANNEL_ID = os.environ["UC_YOUTUBE"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = "@migajasrandom"
THREAD_ID = 4
LAST_VIDEO_FILE = "last_video.txt"

# 1. Buscar el video más reciente que NO sea live
search_url = "https://www.googleapis.com/youtube/v3/search"
params = {
    "key": API_KEY,
    "channelId": CHANNEL_ID,
    "part": "snippet",
    "order": "date",
    "maxResults": 5,
    "type": "video"
}
resp = requests.get(search_url, params=params).json()

print("RESPUESTA COMPLETA:", resp)

video = None
for item in resp.get("items", []):
    if item["snippet"]["liveBroadcastContent"] == "none":
        video = item
        break

if video is None:
    print("No se encontró video sin ser live")
    exit()

video_id = video["id"]["videoId"]
video_title = video["snippet"]["title"]
video_link = f"https://www.youtube.com/watch?v={video_id}"

# 2. Comparar con el último notificado
last_video = ""
if os.path.exists(LAST_VIDEO_FILE):
    with open(LAST_VIDEO_FILE, "r") as f:
        last_video = f.read().strip()

if video_id != last_video:
    message = f"🎥 ¡Nuevo video en el canal!\n\n{video_title}\n{video_link}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "message_thread_id": THREAD_ID,
        "text": message
    }
    requests.post(url, json=payload)

    with open(LAST_VIDEO_FILE, "w") as f:
        f.write(video_id)
    print("Nuevo video notificado")
else:
    print("Sin novedades")
