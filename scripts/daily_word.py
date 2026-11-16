import os, json, html, datetime, tempfile, subprocess
import requests
from gtts import gTTS

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT = os.environ["TELEGRAM_CHAT_ID"]
API = f"https://api.telegram.org/bot{TOKEN}"

here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "words.json"), encoding="utf8") as f:
    words = json.load(f)

# one article per day, cycling through the word list
today = datetime.date.today()
w = words[today.toordinal() % len(words)]
en, pos, km, ex = w["en"], w["pos"], w["km"], w["ex"]

tips = {
    "noun": "ជាពាក្យនាម ដែលប្រើហៅមនុស្ស ទីកន្លែង ឬវត្ថុ។",
    "verb": "ជាពាក្យកិរិយាបទ ដែលប្រើបង្ហាញសកម្មភាព។",
    "adjective": "ជាពាក្យគុណនាម ដែលប្រើពិពណ៌នាអំពីអ្វីមួយ។",
    "adverb": "ជាពាក្យក្រិយាវិសេសនាម ដែលប្រើបញ្ជាក់របៀប ឬពេលវេលា។",
    "phrase": "ជាឃ្លាដែលគេប្រើញឹកញាប់ក្នុងការសន្ទនាប្រចាំថ្ងៃ។",
    "interjection": "ជាពាក្យឧទាន ដែលគេប្រើក្នុងស្ថានការណ៍ផ្សេងៗ។",
}
tip = tips.get(pos, "ជាពាក្យដែលគេប្រើក្នុងការសន្ទនាប្រចាំថ្ងៃ។")

title = f"📖 ពាក្យថ្ងៃនេះ៖ {en}"
p1 = (f"ថ្ងៃនេះយើងនឹងស្គាល់ពាក្យ <b>{html.escape(en)}</b> "
      f"ដែលមានន័យថា <b>{html.escape(km)}</b>។ {html.escape(tip)}")
p2 = ("ពាក្យនេះអាចប្រើបានច្រើនក្នុងជីវិតប្រចាំថ្ងៃ "
      "ទាំងនៅផ្ទះ នៅសាលារៀន ឬពេលនិយាយជាមួយមិត្តភក្តិ។ "
      "បើអ្នករៀនវាឱ្យបានល្អ អ្នកនឹងយល់ និងនិយាយភាសាអង់គ្លេសបានកាន់តែងាយ។")
p3 = f"ជាភាសាអង់គ្លេសយើងអាចនិយាយថា៖ <i>{html.escape(ex)}</i>"
p4 = ("សូមចងចាំ និងនិយាយពាក្យនេះតាមសំឡេងអានខាងក្រោម "
      "ហើយព្យាយាមសរសេរប្រយោគមួយរបស់អ្នកផ្ទាល់ ដើម្បីផ្ញើមកក្នុង channel។")

text = (
    f"<b>{html.escape(title)}</b>\n\n"
    f"{p1}\n\n"
    f"{p2}\n\n"
    f"{p3}\n\n"
    f"{p4}\n\n"
    "🎓 Seng Hour English Academy\n"
    "🔗 https://syu284043-cmd.github.io/seng-hour-english-academy/index%20(2).html"
)

# 1) send the article
r = requests.post(f"{API}/sendMessage", data={
    "chat_id": CHAT,
    "text": text,
    "parse_mode": "HTML",
    "disable_web_page_preview": "true",
}, timeout=30)
r.raise_for_status()

# 2) read the same article aloud (English)
speech = (
    f"Today's word is {en}. It means {km}. "
    f"{ex} "
    f"Listen and repeat after me: {en}. {en}. {en}."
)
tmp = tempfile.gettempdir()
mp3 = os.path.join(tmp, "word_of_the_day.mp3")
ogg = os.path.join(tmp, "word_of_the_day.ogg")
gTTS(text=speech, lang="en", slow=False).save(mp3)

# convert to OGG/Opus so Telegram shows it as a voice message (no cover photo)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp3,
                "-c:a", "libopus", "-b:a", "48k", ogg], check=True)

with open(ogg, "rb") as voice:
    r = requests.post(f"{API}/sendVoice", data={
        "chat_id": CHAT,
        "caption": "🔊 ស្តាប់ និងអានតាម / Listen and repeat",
    }, files={"voice": ("word_of_the_day.ogg", voice, "audio/ogg")}, timeout=90)
r.raise_for_status()
print("sent article and voice:", en)
