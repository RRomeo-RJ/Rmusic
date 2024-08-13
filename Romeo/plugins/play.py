import aiohttp
import asyncio
import os
import random
import aiofiles
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped
from youtubesearchpython import VideosSearch
from PIL import Image, ImageDraw, ImageFont, ImageOps
import yt_dlp
import ffmpeg
from Romeo import app, call_py
from Romeo.active import *
from Romeo.queues import QUEUE, add_to_queue, remove_from_queue

# Define your themes and colors
themes = ["blue", "red", "pink", "purple"]
colors = ["white", "black", "red", "orange", "yellow", "green", "cyan", "azure", "blue", "violet", "magenta", "pink"]

async def bash(command: str):
    """Run a shell command asynchronously and return the output."""
    proc = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    return stdout.decode(), stderr.decode()

def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = f"https://i.ytimg.com/vi/{data['id']}/hqdefault.jpg"
        videoid = data["id"]
        return [songname, url, duration, thumbnail, videoid]
    except Exception as e:
        print(e)
        return 0

async def ytdl(format: str, link: str):
    stdout, stderr = await bash(f'yt-dlp --geo-bypass -g -f "[height<=?720][width<=?1280]" {link}')
    if stdout:
        return 1, stdout.strip()
    return 0, stderr

chat_id = None
DISABLED_GROUPS = []
useer = "NaN"
ACTV_CALLS = []

def transcode(filename):
    ffmpeg.input(filename).output(
        "input.raw", 
        format="s16le", 
        acodec="pcm_s16le", 
        ac=2, 
        ar="48k"
    ).overwrite_output().run()
    os.remove(filename)

def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))

def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

async def generate_cover(thumbnail, title, userid, ctitle):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                async with aiofiles.open(f"thumb{userid}.png", mode="wb") as f:
                    await f.write(await resp.read())

    images = random.choice(themes)
    border = random.choice(colors)

    image1 = Image.open(f"thumb{userid}.png")
    image2 = Image.open(f"Romeo/helper/rj/{images}.png")

    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)

    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")

    Image.alpha_composite(image5, image6).save(f"temp{userid}.png")

    logo = Image.open(f"temp{userid}.png")
    img = ImageOps.expand(logo, border=10, fill=f"{border}")

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("Romeo/helper/rj/font.otf", 55)
    font2 = ImageFont.truetype("Romeo/helper/rj/font.otf", 35)

    # Placeholder for duration and views
    duration = "Unknown"
    views = "Unknown"

    draw.text((20, 555), f"Title: {title[:50]} ...", (255, 255, 255), font=font)
    draw.text((20, 615), f"Duration: {duration}", (255, 255, 255), font=font)
    draw.text((20, 675), f"Views: {views}", (255, 255, 255), font=font)
    draw.text((10, 10), f"RJ•MUSIC", (255, 255, 255), font=font2)

    img.save(f"final{userid}.png")
    os.remove(f"temp{userid}.png")
    os.remove(f"thumb{userid}.png") 

    return f"final{userid}.png"

@Client.on_message(filters.command(["play", "ply"]) & filters.group)
async def play(c: Client, m: Message):
    await m.delete()
    replied = m.reply_to_message
    chat_id = m.chat.id
    _assistant = await get_assistant(chat_id, "assistant")
    assistant = _assistant["saveassistant"]
    
    if replied:
        if replied.audio or replied.voice:
            romeo = await replied.reply("📥 **downloading audio...**")
            dl = await replied.download()
            link = replied.link
            if replied.audio:
                if replied.audio.title:
                    songname = replied.audio.title[:70]
                else:
                    if replied.audio.file_name:
                        songname = replied.audio.file_name[:70]
                    else:
                        songname = "Audio"
            elif replied.voice:
                songname = "Voice Note"

            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await romeo.delete()
                await m.reply_photo(
                    photo=f"{QUE_IMG}",
                    caption=f"💡 **Track added to queue »** `{pos}`\n\n🏷 **Name:** [{songname}]({link}) | `music`\n💭 **Chat:** `{chat_id}`\n🎧 **Request by:** {m.from_user.mention()}"
                )
            else:
                try:
                    await call_py.join_group_call(chat_id, AudioPiped(dl), stream_type=StreamType(local_stream=True))
                    await add_active_chat(chat_id)
                    add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                    await romeo.delete()
                    requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                    await m.reply_photo(
                        photo=f"{PLAY_IMG}",
                        caption=f"🏷 **Name:** [{songname}]({link})\n💭 **Chat:** `{chat_id}`\n💡 **Status:** `Playing`\n🎧 **Request by:** {requester}\n📹 **Stream type:** `Music`"
                    )
                except Exception as e:
                    await romeo.delete()
                    await m.reply_text(f"🚫 error:\n\n» {e}")
        else:
            if len(m.command) < 2:
                await m.reply_text(f"💬**Usage: /play Give a Title Song To Play Music or /vplay for Video Play**")
            else:
                romeo = await m.reply_text(f"**Downloading**\n\n0% ▓▓▓▓▓▓▓▓▓▓▓▓ 100%")
                query = m.text.split(None, 1)[1]
                search = ytsearch(query)
                if search == 0:
                    await romeo.edit("💬 **no results found.**")
                else:
                    songname = search[0]
                    title = search[0]
                    url = search[1]
                    duration = search[2]
                    thumbnail = search[3]
                    videoid = search[4]
                    userid = m.from_user.id
                    gcname = m.chat.title
                    ctitle = await CHAT_TITLE(gcname)
                    image = await play_thumb(videoid)
                    queuem = await queue_thumb(videoid)
                    format = "bestaudio"
                    abhi, ytlink = await ytdl(format, url)
                    if abhi == 0:
                        await romeo.edit(f"💬 yt-dl issues detected\n\n» `{ytlink}`")
                    else:
                        if chat_id in QUEUE:
                            pos = add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                            await romeo.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_photo(
                                photo=queuem,
                                caption=f"💡 **Track added to queue »** `{pos}`\n\n🏷 **Name:** [{songname[:22]}]({url}) | `music`\n**⏱ Duration:** `{duration}`\n🎧 **Request by:** {requester}"
                            )
                        else:
                            try:
                                cover = await generate_cover(thumbnail, title, userid, ctitle)
                                await call_py.join_group_call(chat_id, AudioPiped(ytlink), stream_type=StreamType(local_stream=True))
                                await add_active_chat(chat_id)
                                add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                                await romeo.delete()
                                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                                await m.reply_photo(
                                    photo=cover,
                                    caption=f"🏷 **Name:** [{songname[:22]}]({url})\n💭 **Chat:** `{chat_id}`\n💡 **Status:** `Playing`\n🎧 **Request by:** {requester}\n📹 **Stream type:** `Music`"
                                )
                                os.remove(cover)
                            except Exception as e:
                                await romeo.delete()
                                await m.reply_text(f"🚫 error:\n\n» {e}")

@Client.on_message(filters.command(["skip"]) & filters.group)
@AssistantAdd
async def skip(c: Client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        await call_py.leave_group_call(chat_id)  # Stop the current stream
        remove_from_queue(chat_id)  # Remove the current song from the queue
        if QUEUE[chat_id]:
            next_song = QUEUE[chat_id][0]  # Get the next song
            songname, ytlink, url, song_type, _ = next_song
            try:
                await call_py.join_group_call(chat_id, AudioPiped(ytlink), stream_type=StreamType(local_stream=True))
                await add_active_chat(chat_id)
                await m.reply_text(f"🎶 **Skipped to next track:** {songname}")
            except Exception as e:
                await m.reply_text(f"🚫 error:\n\n» {e}")
        else:
            await m.reply_text("🔄 The queue is empty. No more tracks to play.")
    else:
        await m.reply_text("🚫 No song is currently playing.")

