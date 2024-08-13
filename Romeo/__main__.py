import asyncio
import importlib
from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall
from Romeo import client, app, call_py, LOGGER
from Romeo.plugins import ALL_MODULES


async def start_bot():
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("Romeo.plugins" + all_module)
    LOGGER("plugins").info("Successfully Imported Modules...")
    await client.start()
    await call_py.start()
    
    LOGGER("Romeo").info(
        "bot started"
    )
    await idle()
    await app.stop()
    await client.stop()
    LOGGER("Romeo").info("Stopping Music Bot...")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_bot())
