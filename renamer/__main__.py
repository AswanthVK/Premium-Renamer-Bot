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
LOGGER = logging.getLogger(__name__)


isUserPremium = False
if len(Config.STRING_SESSION) > 10:
    if userBot := Client(
        "Tele-UserBot",
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        session_string=Config.STRING_SESSION,
    ):
        userBot.start()
        if (userBot.get_me()).is_premium:
            isUserPremium = True
            LOGGER.info("[SUCCESS] Initiated UserBot : Premium Mode") #Logging is Needed Very Much
        else:
            isUserPremium = False
            LOGGER.info("[SUCCESS] Initiated UserBot : Non-Premium Mode. Add Premium Account StringSession to Use 4GB Upload. ")
    else:
        LOGGER.warning("[FAILED] Userbot Not Started. ReCheck Your STRING_SESSION, and Other Vars")
else: LOGGER.info("Provide or ReGenerate Your STRING_SESSION Var")


if __name__ == "__main__" :


    plugins = dict(root="renamer/plugins")
    Renamer = Client(
        "DKBOTZ",
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






