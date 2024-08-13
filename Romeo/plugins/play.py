import aiohttp
import aiofiles
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.types.input_stream import AudioPiped
import yt_dlp
import subprocess
from Romeo import app, call_py as pytgcalls


def bash(command):
    """Run a shell command and return the output."""
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode(), result.stderr.decode()

async def ytdl(link: str):
    """Download the audio from a YouTube link using yt-dlp."""
    stdout, stderr = bash(f'yt-dlp -g -f "[height<=?720][width<=?1280]" {link}')
    if stderr:
        print(f"Error: {stderr}")
    return stdout.strip() if stdout else None

async def download_audio(url: str, file_path: str):
    """Download the audio file from a URL."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                async with aiofiles.open(file_path, 'wb') as f:
                    await f.write(await resp.read())

async def play_song(chat_id: int, url: str):
    """Play the song in a voice chat."""
    audio_url = await ytdl(url)
    if audio_url:
        await pytgcalls.join_group_call(
            chat_id,
            AudioPiped(audio_url),
            stream_type=StreamType().local_stream
        )
        return "Playing the song."
    return "Failed to download or play the song."

@app.on_message(filters.command("play") & filters.group)
async def handle_play(client: Client, message: Message):
    """Handle the /play command in any group."""
    if len(message.command) < 2:
        await message.reply_text("Usage: /play <YouTube URL>")
        return

    url = message.command[1]
    chat_id = message.chat.id
    response = await play_song(chat_id, url)
    await message.reply_text(response)
