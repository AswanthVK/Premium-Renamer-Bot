import asyncio
import logging

from pyrogram import idle

from renamer.config import Config
from renamer.__main__ import USERBOT

logger = logging.getLogger(__name__)

loop = asyncio.get_event_loop()


async def booted(bot):
    chats = Config.AUTH_USERS

    try:
        logger.info(f"Added Counting")
    except Exception as e:
        logger.info(f"⚠️ Main Error: {e}")

    for i in chats:
        try:
            await bot.send_message(i, "The Bot is Restarted ♻️ Now")
        except Exception:
            logger.info(f"⚠️ Not found id {i}")


async def start_bots():
    print("Processing.....")
    '''   
    try:
        await BOT.start()
        logger.info(f"Bot is Running....🏃‍♂️")
    except Exception as e:
        logger.info(f"⚠️ Bot Error: {e}")
    '''
  
    if Config.SESSION_STRING:
        try:
            await USERBOT.start()
            logger.info(f"UserBot is Running....🏃")
        except Exception as e:
            logger.info(f"⚠️ UserBot Error: {e}")

    await idle()


if __name__ == "__main__":
    try:
        loop.run_until_complete(start_bots())
    except KeyboardInterrupt:
        logger.info(f"⚠️ Bots Stopped!! Problem in loop run")
