import os
import json
import gspread
from google.oauth2.service_account import Credentials
from telethon import TelegramClient, events
from flask import Flask
from threading import Thread
import datetime

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
service_account_info = json.loads(os.environ['SERVICE_ACCOUNT_JSON'])

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

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
    "@dubai_oae_expats
