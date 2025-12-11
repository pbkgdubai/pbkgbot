import os
import json
import gspread
from google.oauth2.service_account import Credentials
from telethon import TelegramClient, events
from flask import Flask
from threading import Thread
import datetime
import asyncio

# -----------------------------
# Flask server for UptimeRobot
# -----------------------------
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()


# -----------------------------
# Google Sheets connection via Render Secret
# -----------------------------
SERVICE_ACCOUNT_JSON = os.environ.get("SERVICE_ACCOUNT_JSON")
if not SERVICE_ACCOUNT_JSON:
    raise RuntimeError("SERVICE_ACCOUNT_JSON not found in environment variables!")

service_account_info = json.loads(SERVICE_ACCOUNT_JSON)

scopes = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)

client_gs = gspread.authorize(creds)

GOOGLE_SHEET_NAME = "Telegram Leads"
sheet = client_gs.open(GOOGLE_SHEET_NAME).sheet1


# -----------------------------
# Telegram credentials
# -----------------------------
api_id = 38436869
api_hash = "8ce925bc64c01445a7463faf4703a3c9"

client = TelegramClient("pbkg_session", api_id, api_hash)


# -----------------------------
# Groups and Keywords
# -----------------------------
GROUPS = [
    "@chat_dubai_group", "@nedvizhimost_dubai_rent", "@dubaichat_russkie",
    "@russians_v_dubai", "@uslugi_v_dubai", "@ru_chat_uae", "@nedviga_dubai",
    "@uaechatt", "@Uaechattings", "@dubai_tysa", "@dubairealtyinvest",
    "@dubai_oae_expats", "@kazakhindubai", "@DubaiOAE_chat", "@biznesuae",
    "@Afisa_dubai", "@dubai_chat", "@my_dubai_chat", "@dubai_chat_russkie",
    "@russkie_in_dubai", "@dubai_rr", "@dubai_bgchat", "@uae_dubai",
    "@dubai_netv", "@uae_dudai", "@dubayo", "@dubai_uae_chat",
    "@ukrainci_v_dubaii", "@chatrusdubai", "@abudabi_chat", "@dubai_em",
    "@poisk_dubai", "@dubai_nedvizhimost_arenda_biznes", "@my_dubai_chat",
    "@dubai_rr", "@dubaiChat4", "@dubai_netv", "@dubai_chat",
    "@prod_dubai", "@dubai_oae_ru", "@chat_dubai_oae", "@DubaiOAE_chat1",
    "@dubai_em", "@poisk_dubai", "@uae_architects", "@design467"
]

KEYWORDS = [
    "ремонт", "ремонта", "мастер", "мастера", "починить", "дизайн", "интерьер",
    "сантехник", "электрик", "отделка", "renovation", "fit out", "maintenance",
    "contractor", "ремонтом"
]


# -----------------------------
# Telegram message handler
# -----------------------------
@client.on(events.NewMessage())
async def handler(event):
    chat = await event.get_chat()
    chat_title = getattr(chat, 'title', "unknown")

    if event.chat_id and chat_title:
        if (chat.username and f"@{chat.username}".lower() in [g.lower() for g in GROUPS]) or \
           (chat_title.lower() in [g.lower().replace("@", "") for g in GROUPS]):

            message_text = event.raw_text.lower()
            if any(keyword in message_text for keyword in KEYWORDS):
                user = await event.get_sender()
                row = [
                    str(datetime.datetime.now()),
                    chat_title,
                    user.username if user.username else "no username",
                    event.raw_text
                ]
                sheet.append_row(row)
                print("🔥 NEW LEAD saved to Google Sheets:", row)


# -----------------------------
# Main runner
# -----------------------------
async def main():
    print("Bot is running and monitoring groups...")
    await client.run_until_disconnected()


# Start Flask server
keep_alive()

# Run Telegram bot
with client:
    client.loop.run_until_complete(main())
