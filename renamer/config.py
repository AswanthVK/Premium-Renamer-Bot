import os

class Config:
    ACTIVE_DOWNLOADS = {}
    API_ID = int(os.environ.get("API_ID", '6795023'))
    API_HASH = os.environ.get("API_HASH", '48eb04ae416967495ba9930f87d4f4da')
    PAID_BOT = os.environ.get("PAID_BOT", "YES")
    SESSION_STRING = os.environ.get("SESSION_STRING")
    AUTH_USERS =  [int(i) for i in os.environ.get("AUTH_USERS", "1805398747").split(" ")]
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "5028427286:AAGggDShZZwX7lnfkeaH9i0FalwBBkh2cGU")
    DATABASE_URL = os.environ.get("DATABASE_URL", "mongodb+srv://dkbotz:786@cluster0.pczec.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    DOWNLOAD_LOCATION = "./DOWNLOADS"
    DB_CHANNEL_ID = -1001769216579
    RESTART_TIME = []
    TIME_GAP1 = {}
    TIME_GAP2 = {}
    timegap_message = {}
