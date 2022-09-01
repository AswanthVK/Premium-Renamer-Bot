import logging
import logging.config

# Get logging configurations
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

import os
import pytz
import datetime
from .config import Config
from pyrogram import Client
from .database.database import Database
from pyromod import listen



logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


if Config.SESSION_STRING:
    USERBOT = Client(
        "cmuserbot",
        session_string=Config.SESSION_STRING,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
    )
else:
    USERBOT = None


if __name__ == "__main__" :


    plugins = dict(root="renamer/plugins")
    Renamer = Client(
        "Uploader Bot",
        bot_token=Config.BOT_TOKEN,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        plugins=plugins)

    if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)

    time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
    Config.RESTART_TIME.append(time)

    Renamer.db = Database(Config.DATABASE_URL, 'renamerV3')
    Renamer.broadcast_ids = {}
    Renamer.run()






