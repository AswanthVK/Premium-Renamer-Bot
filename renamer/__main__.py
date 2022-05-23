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


def main():

    Renamer = Client("Renamer_NsBot",
                 bot_token=Config.BOT_TOKEN,
                 api_id=Config.API_ID,
                 api_hash=Config.API_HASH,
                 plugins=dict(root="renamer/plugins"),
                 workers=16)

    if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)

    time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
    Config.RESTART_TIME.append(time)

    Renamer.db = Database(Config.DATABASE_URL, 'renamerV3')
    Renamer.broadcast_ids = {}
    Renamer.run()


if __name__ == "__main__":
    main()



