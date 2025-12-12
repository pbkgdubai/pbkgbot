from telethon import TelegramClient
import asyncio

api_id = 38436869
api_hash = '8ce925bc64c01445a7463faf4703a3c9'

client = TelegramClient('pbkg_session', api_id, api_hash)

async def main():
    await client.start()  # при запуске спросит номер и код из Telegram
    print("✅ Session создана!")

with client:
    client.loop.run_until_complete(main())




