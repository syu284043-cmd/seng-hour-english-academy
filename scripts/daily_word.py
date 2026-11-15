import os, json, html, datetime, tempfile
import requests
from gtts import gTTS

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT = os.environ["TELEGRAM_CHAT_ID"]
API = f"https://api.telegram.org/bot{TOKEN}"

here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "words.json"), encoding="utf8") as f:
    words = json.load(f)

# one word per day, cycling through the list
today = datetime.date.today()
w = words[today.toordinal() % len(words)]

text = (
    "📘 <b>ពាក្យថ្ងៃនេះ / Word of the Day</b>\n\n"
    f"🔤 <b>{html.escape(w['en'])}</b> <i>({html.escape(w['pos'])})</i>\n"
    f"🇰🇭 {html.escape(w['km'])}\n\n"
    f"💬 <i>{html.escape(w['ex'])}</i>\n\n"
    "🎓 Seng Hour English Academy\n"
    "🔗 https://syu284043-cmd.github.io/seng-hour-english-academy/index%20(2).html"
)

# 1) send the text message
r = requests.post(f"{API}/sendMessage", data={
    "chat_id": CHAT,
    "text": text,
    "parse_mode": "HTML",
    "disable_web_page_preview": "true",
}, timeout=30)
r.raise_for_status()

# 2) create a spoken version (English) and send it as a playable audio message
speech = f"{w['en']}. {w['ex']}"
mp3 = os.path.join(tempfile.gettempdir(), "word_of_the_day.mp3")
gTTS(text=speech, lang="en", slow=False).save(mp3)

with open(mp3, "rb") as audio:
    r = requests.post(f"{API}/sendAudio", data={
        "chat_id": CHAT,
        "title": w["en"],
        "performer": "Seng Hour English Academy",
        "caption": "🔊 ស្តាប់ និងអានតាម / Listen and repeat",
    }, files={"audio": ("word_of_the_day.mp3", audio, "audio/mpeg")}, timeout=90)
r.raise_for_status()
print("sent word and audio:", w["en"])
