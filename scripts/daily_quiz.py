import os, json, html, datetime, urllib.request, urllib.parse

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT = os.environ["TELEGRAM_CHAT_ID"]

here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "quiz.json"), encoding="utf8") as f:
    quizzes = json.load(f)

# one quiz per day, cycling through the list
today = datetime.date.today()
item = quizzes[today.toordinal() % len(quizzes)]

# Telegram limits: question 300 chars, option 100 chars, explanation 200 chars
question = ("🧠 លំហាត់ថ្ងៃនេះ / Quiz of the Day\n\n" + item["q"])[:300]
options = [o[:100] for o in item["options"]]
explanation = ("✅ " + item["explain"])[:200]

data = urllib.parse.urlencode({
    "chat_id": CHAT,
    "question": question,
    "options": json.dumps(options, ensure_ascii=False),
    "type": "quiz",
    "correct_option_id": item["answer"],
    "explanation": explanation,
    "is_anonymous": "true",
}).encode()

req = urllib.request.Request(f"https://api.telegram.org/bot{TOKEN}/sendPoll", data=data)
with urllib.request.urlopen(req, timeout=30) as r:
    print(r.read().decode())
