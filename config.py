from os import getenv

API_ID = int(getenv("API_ID", "14246641"))
API_HASH = getenv("API_HASH", "6f0711cf1fac7dbb09a2bed95c36e673")
BOT_TOKEN = getenv("BOT_TOKEN", "5523050102:AAGMKcLXgDC5V5T0bc5oXiWqjLRKxo7s69M")
OWNER_ID = int(getenv("OWNER_ID", "1720551159"))
STRING_SESSION = getenv("STRING_SESSION", "BQEiZi4AGX0TPy0yaUm4jRlsd1wShK-QLWynh-CwJkz1IPdPjLtMXYS9ecBEdh0bk6em6qEIEKJ0CsMVLs9cXfXkN-K9JYLMeTnD167myMOTCF9b-9X_AuEzwaPfgTgRTZorgCqlwwHc0vtD1v2qQTXmOCm9Oq1Krm16LbGW-QfTiO7bbmJz8Dabr6BIZFtsDI2aZGih1Iv6e53xsnh9NZdymWGWAYJR8IvWY2_7QyzcZzQ4wshPW3xQBlRprbcOO0T6-QvvkuLLEnXBQeTL7F8o1VX4ppWyP0O-u2LgcApKXDWySDYy_yWXfbz74AUh5hQefoXeT7Kieko9FM8N3ejPUCaktwAAAABmjYb3AA")
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "").split()))
ALIVE_PIC = getenv("ALIVE_PIC", "https://telegra.ph/file/e745fdaf1966f228582dc.jpg")
REPO_URL = getenv("REPO_URL", "https://github.com/RRomeo-RJ/Rmusic")
BRANCH = getenv("BRANCH", "main")
LOG_FILE_NAME = "logs.txt"
BOT_NAME = getenv("BOT_NAME", "Umk")
PLAY_IMG = getenv("PLAY_IMG", "https://telegra.ph/file/10b1f781170b1e1867f68.png")
QUE_IMG = getenv("QUE_IMG", "https://telegra.ph/file/b95c13eef1ebd14dbb458.png")
CMD_IMG = getenv("CMD_IMG", "https://telegra.ph/file/66518ed54301654f0b126.png")
