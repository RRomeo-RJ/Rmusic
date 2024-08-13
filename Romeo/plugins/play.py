import aiohttp
import aiofiles
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped
import yt_dlp
from Romeo import app, call_py
import asyncio
from collections import deque
import os

# Queue to hold songs
song_queue = deque()
is_playing = False
skip_flag = False


async def ytdl(link: str):
    """Get the direct URL for audio and thumbnail from a YouTube link using yt-dlp."""
    try:
        # Extract info using yt-dlp
        ydl = yt_dlp.YoutubeDL()
        info = ydl.extract_info(link, download=False)
        audio_url = info.get("url", None)
        thumbnail_url = info.get("thumbnail", None)
        return audio_url, thumbnail_url
    except Exception as e:
        print(f"Error extracting info: {e}")
        return None, None

async def download_audio(url: str, file_path: str):
    """Download the audio file from a URL."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                async with aiofiles.open(file_path, 'wb') as f:
                    await f.write(await resp.read())
            else:
                print(f"Failed to download audio: HTTP {resp.status}")

async def download_thumbnail(url: str, file_path: str):
    """Download the thumbnail image from a URL."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                async with aiofiles.open(file_path, 'wb') as f:
                    await f.write(await resp.read())
            else:
                print(f"Failed to download thumbnail: HTTP {resp.status}")

async def play_song(chat_id: int, file_path: str):
    """Play the song in a voice chat."""
    await call_py.join_group_call(
        chat_id,
        AudioPiped(file_path),
        stream_type=StreamType().local_stream
    )

async def stop_playback():
    """Stop current playback."""
    global skip_flag
    skip_flag = True
    await call_py.leave_group_call()

async def process_queue(client: Client, chat_id: int):
    """Process songs in the queue and play them one by one."""
    global is_playing, skip_flag
    if is_playing:
        return
    is_playing = True
    skip_flag = False
    
    while song_queue:
        if skip_flag:
            skip_flag = False
            continue
        
        url, file_path, thumbnail_path = song_queue.popleft()
        audio_url, thumbnail_url = await ytdl(url)
        if audio_url:
            await download_audio(audio_url, file_path)
            if thumbnail_url:
                await download_thumbnail(thumbnail_url, thumbnail_path)
                await client.send_photo(chat_id, thumbnail_path, caption=f"Now playing: {url}")
            else:
                await client.send_message(chat_id, f"Now playing: {url}")
            await play_song(chat_id, file_path)
            await asyncio.sleep(10)  # Adjust this as needed for the song duration
            os.remove(thumbnail_path)  # Clean up thumbnail file after sending
        else:
            print(f"Failed to get URL for {url}")
    
    is_playing = False

@app.on_message(filters.command("play") & filters.group)
async def handle_play(client: Client, message: Message):
    """Handle the /play command in any group."""
    await message.delete()

    if len(message.command) < 2:
        await message.reply_text("Usage: /play <YouTube URL>")
        return

    url = message.command[1]
    chat_id = message.chat.id
    file_path = f'audio_file_{len(song_queue)}.mp3'  # Unique file name for each song
    thumbnail_path = f'thumbnail_{len(song_queue)}.jpg'  # Unique file name for each thumbnail

    song_queue.append((url, file_path, thumbnail_path))
    await message.reply_text(f"Added to queue: {url}")

    if not is_playing:
        await process_queue(client, chat_id)

@app.on_message(filters.command("skip") & filters.group)
async def handle_skip(client: Client, message: Message):
    """Handle the /skip command to skip the current song."""
    await message.delete()
    if is_playing:
        await stop_playback()
        await message.reply_text("Song skipped.")
        await process_queue(client, message.chat.id)
    else:
        await message.reply_text("No song is currently playing.")
