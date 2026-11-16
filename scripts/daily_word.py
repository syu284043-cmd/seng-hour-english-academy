import os, json, html, datetime
import requests

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT = os.environ["TELEGRAM_CHAT_ID"]
API = f"https://api.telegram.org/bot{TOKEN}"

here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "words.json"), encoding="utf8") as f:
    words = json.load(f)

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
p4 = ("សូមចងចាំពាក្យនេះ ហើយព្យាយាមសរសេរប្រយោគមួយរបស់អ្នកផ្ទាល់ "
      "ដើម្បីផ្ញើមកក្នុង channel។")

text = (
    f"<b>{html.escape(title)}</b>\n\n"
    f"{p1}\n\n{p2}\n\n{p3}\n\n{p4}\n\n"
    "🎓 Seng Hour English Academy\n"
    "🔗 https://syu284043-cmd.github.io/seng-hour-english-academy/index%20(2).html"
)

r = requests.post(f"{API}/sendMessage", data={
    "chat_id": CHAT, "text": text, "parse_mode": "HTML",
    "disable_web_page_preview": "true",
}, timeout=30)
r.raise_for_status()
print("sent article:", en)
