import os, json, html, datetime, urllib.request, urllib.parse

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT = os.environ["TELEGRAM_CHAT_ID"]

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

data = urllib.parse.urlencode({
    "chat_id": CHAT,
    "text": text,
    "parse_mode": "HTML",
    "disable_web_page_preview": "true",
}).encode()

req = urllib.request.Request(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data=data)
with urllib.request.urlopen(req, timeout=30) as r:
    print(r.read().decode())
