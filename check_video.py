import feedparser
import requests
import os
import json

CHANNEL_ID = os.environ["UC_YOUTUBE"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = "@migajasrandom"
THREAD_ID = 4
LAST_VIDEO_FILE = "last_video.txt"

feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
feed = feedparser.parse(feed_url)
latest = feed.entries[0]
video_id = latest.yt_videoid
video_title = latest.title
video_link = latest.link

# Leer el último video ya notificado
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
