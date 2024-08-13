from os import getenv

API_ID = int(getenv("API_ID", "14246641"))
API_HASH = getenv("API_HASH", "")
BOT_TOKEN = getenv("BOT_TOKEN", "")
OWNER_ID = int(getenv("OWNER_ID", ""))
STRING_SESSION = getenv("STRING_SESSION", "")
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "").split()))
ALIVE_PIC = getenv("ALIVE_PIC", "https://telegra.ph/file/e745fdaf1966f228582dc.jpg")
REPO_URL = getenv("REPO_URL", "https://github.com/RRomeo-RJ/Rmusic")
BRANCH = getenv("BRANCH", "main")
LOG_FILE_NAME = "logs.txt"
BOT_NAME = getenv("BOT_NAME", "Umk")
