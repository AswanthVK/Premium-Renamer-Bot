import os

class Config:
    ACTIVE_DOWNLOADS = {}
    API_ID = int(os.environ.get("API_ID", 12345))
    API_HASH = os.environ.get("API_HASH")
    AUTH_USERS =  [int(i) for i in os.environ.get("AUTH_USERS", "").split(" ")]
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    DATABASE_URL = os.environ.get("DATABASE_URL", "")
    DOWNLOAD_LOCATION = "./DOWNLOADS"
    DB_CHANNEL_ID = -1001602376426
    RESTART_TIME = []
    TIME_GAP1 = {}
    TIME_GAP2 = {}
    timegap_message = {}
