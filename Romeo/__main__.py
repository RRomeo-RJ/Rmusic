import asyncio
import importlib
from pyrogram import Client, idle
from Romeo import client, app, call_py

async def start_bot():
    await app.start()
    print("LOG: Founded Bot token Booting..")
    print("USERBOT SUCCESSFULLY STARTED ✅✅")
    await client.start()
    await call_py.start()
    await idle()

loop = asyncio.get_event_loop()
loop.run_until_complete(start_bot())
