import os
import sys
import asyncio
from time import time
from datetime import datetime
from pyrogram import __version__, filters, Client
from pyrogram.types import Message
from platform import python_version
from Romeo import SUDO_USER
from config import*

START_TIME = datetime.utcnow()
TIME_DURATION_UNITS = (
    ('Week', 60 * 60 * 24 * 7),
    ('Day', 60 * 60 * 24),
    ('Hour', 60 * 60),
    ('Min', 60),
    ('Sec', 1)
)
async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)

@app.on_message(filters.command(["start", "st"], ".") & filters.private)
async def start(client: Client, message: Message):
    await message.delete()
    txt = (
        f"**━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🥀 𝐇𝐞𝐥𝐥𝐨,\n"
        f"𝐈'𝐦 𝐀 𝐌𝐮𝐬𝐢𝐜 𝐁𝐨𝐭\n"
        f"𝐏𝐥𝐚𝐲 𝐀𝐮𝐝𝐢𝐨 𝐀𝐧𝐝 𝐕𝐢𝐝𝐞𝐨 𝐖𝐢𝐭𝐡𝐨𝐮𝐭 𝐋𝐚𝐠𝐬\n"
        f"𝐄𝐧𝐣𝐨𝐲 𝐘𝐨𝐮𝐫 𝐦𝐮𝐬𝐢𝐜 24*7.\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━**"    
    )
    await message.reply_photo(photo=ALIVE_PIC, caption=txt) 


@app.on_message(filters.command(["alive"], ".") & filters.private)
async def alive(client: Client, message: Message):
    start = time()
    current_time = datetime.utcnow()
    ping = time() - start
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    txt = (
        f"❥︎ 𝐀𝐋𝐈𝐕𝐄 ☟︎︎︎\n\n"
        f"🇻𝐄𝐑𝐒𝐈𝐎𝐍 ❥︎ 1.0\n"
        f"🇵𝐈𝐍𝐆 ❥︎ {ping * 1000:.3f}ᴍs\n"
        f"🇺𝐏★🇹𝐈𝐌𝐄 ❥︎ {uptime}\n"
        f"🇵𝐘𝐓𝐇𝐎𝐍 ❥︎ {python_version()}`\n"
        f"🇵𝐘𝐑𝐎𝐆𝐑𝐀𝐌 ❥︎ {__version__}\n"
        f"🇴𝐖𝐍𝐄𝐑 ❥︎ {client.me.mention}"    
    )
    await message.delete()
    await message.reply_photo(photo=ALIVE_PIC, caption=txt)

@app.on_message(filters.command(["ping"], ".") & filters.private)
async def ping(client: Client, message: Message):
    r = await message.reply_text("**🇵𝐎𝐍𝐆**")
    start = time()
    current_time = datetime.utcnow()
    ping = time() - start
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.delete()
    await r.edit(
        f"★ 🇸𝐖𝐀𝐆𝐀𝐓★🇳𝐇𝐈★🇰𝐀𝐑𝐎𝐆𝐄★🇭𝐀𝐌𝐀𝐑𝐀 ★\n\n"
        f"🇵𝐈𝐍𝐆 ❥︎ {ping * 1000:.3f}ᴍs\n"
        f"🇺𝐏★🇹𝐈𝐌𝐄 ❥︎ {uptime}\n"
        f"🇴𝐖𝐍𝐄𝐑 ❥︎ {client.me.mention}"
    )
