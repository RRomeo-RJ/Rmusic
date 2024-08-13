import aiohttp
import aiofiles
import subprocess
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.types.input_stream import AudioPiped
import yt_dlp
from Romeo import app, call_py as pytgcalls
import asyncio
from collections import deque
import os

# Queue to hold songs
song_queue = deque()
is_playing = False

def bash(command):
    """Run a shell command and return the output."""
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode(), result.stderr.decode()

async def ytdl(link: str):
    """Get the direct URL for audio and thumbnail from a YouTube link using yt-dlp."""
    # Get video info
    stdout, stderr = bash(f'yt-dlp -j {link}')
    if stderr:
        print(f"Error: {stderr}")
        return None, None

    info = yt_dlp.YoutubeDL().extract_info(link, download=False)
    audio_url = info.get("url", None)
    thumbnail_url = info.get("thumbnail", None)
    
    return audio_url, thumbnail_url

async def download_audio(url: str, file_path: str):
    """Download the audio file from a URL."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                async with aiofiles.open(file_path, 'wb') as f:
                    await f.write(await resp.read())

async def download_thumbnail(url: str, file_path: str):
    """Download the thumbnail image from a URL."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                async with aiofiles.open(file_path, 'wb') as f:
                    await f.write(await resp.read())

async def play_song(chat_id: int, file_path: str):
    """Play the song in a voice chat."""
    await pytgcalls.join_group_call(
        chat_id,
        AudioPiped(file_path),
        stream_type=StreamType().local_stream
    )

async def process_queue(client: Client, chat_id: int):
    """Process songs in the queue and play them one by one."""
    global is_playing
    if is_playing:
        return
    is_playing = True
    
    while song_queue:
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
