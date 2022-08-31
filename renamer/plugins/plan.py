import asyncio
import datetime
import io
import logging
import os
import random
import string
import time
import traceback
from ..config import Config
import aiofiles
from pyrogram import Client, filters
from pyrogram.errors import (
    FloodWait,
    InputUserDeactivated,
    PeerIdInvalid,
    UserIsBlocked,
)

log = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


@Client.on_message(filters.private & filters.command("plan"))
async def help(c, m):
    user_id = m.from_user.id
    if Config.PAID_BOT.upper() == "YES":
        try:
            paid_status = await c.db.get_paid_status(user_id)
        except:
            await update.reply("⚠️ First Click on /start, Then try again")
            return
        if paid_status["is_paid"]:
            current_date = datetime.datetime.now()
            paid_duration = paid_status["paid_duration"]
            paid_on = paid_status["paid_on"]
            paid_reason = paid_status["paid_reason"]
            integer_paid_duration = int(paid_duration)
            will_expire = paid_on + datetime.timedelta(days=integer_paid_duration)
            if will_expire < current_date:
                try:
                    await c.db.remove_paid(user_id)
                except Exception as e:
                    logger.info(f"⚠️ Error: {e}")
                try:
                    await bot.send_message(
                        update.chat.id,
                        f"**User Id:** `{m.from_user.id}`\n\n**User Name:** @{m.from_user.username}\n\n**Plan Validity:** `{paid_duration}` Days\n\n**Joined On** : `{paid_on}`\n\n👋 Your Paid Plan Has Expired On {will_expire}\n\nIf You Want To Use The Bot, You Can Do So By Paying.\n\n__**Plan 1**__\n\n`49/M\n\nAll Features Of This Bot`\n\n__**Plan 2**__\n\n`130 For 3 Month\n\nAll Features Of This Bot`\n\n__**Plan 2**__\n\n`500 For 1 Year\n\nAll Features Of This Bot`\n\n||**Need More Plans Contact To Our Developer :- @DKBOTZHELP**||",
                    )
                except Exception as e:
                    logger.info(f"⚠️ Error: {e}")
                for i in Config.AUTH_USERS:
                    try:
                        await bot.send_message(
                            i,
                            f"🌟 **Plan Expired:** \n\n**User Id:** `{m.from_user.id}`\n\n**User Name:** @{update.from_user.username}\n\n**Plan Validity:** {paid_duration} Days\n\n**Joined On** : {paid_on}\n\n**Discription** : {paid_reason}",
                        )
                    except Exception:
                        logger.info(f"⚠️ Not found id {i}")
                return

            else:
                pass

        else:
            current_date = datetime.datetime.now()
            await m.reply_text(
                text="**Your Plan Deatails**\n\n**User Id:** `{m.from_user.id}`\n\n**User Name:** @{m.from_user.username}\n\nPlan : `Free`\n\n**Plan Validity:** `Lifetime`\n\nDate :- {current_date}\n\n__**Plan 1**__\n\n`49/M\n\nAll Features Of This Bot`\n\n__**Plan 2**__\n\n`130 For 3 Month\n\nAll Features Of This Bot`\n\n__**Plan 2**__\n\n`500 For 1 Year\n\nAll Features Of This Bot`\n\n||**Need More Plans Contact To Our Developer :- @DKBOTZHELP**||",
                reply_markup=SUB_BUTTONS,
                disable_web_page_preview=True,
                quote=True,
            )
            return
    paid_id = m.from_user.id
    paid_status = await c.db.get_paid_status(paid_id)
    if paid_status["is_paid"]:
        current_date = datetime.datetime.now()
        paid_duration = paid_status["paid_duration"]
        paid_on = paid_status["paid_on"]
        paid_reason = paid_status["paid_reason"]
        integer_paid_duration = int(paid_duration)
        will_expire = paid_on + datetime.timedelta(days=integer_paid_duration)
        await m.reply_text(
            text="**Your Plan Deatails**\n\n**User Id:** `{m.from_user.id}`\n\n**User Name:** @{m.from_user.username}\n\nPlan Type : `Paid`\n\n**Plan Validity:** `{paid_duration}` Days\n\n**Plan Buy On** : `{paid_on}`\n\n**Plan Discription** : `{paid_reason}`\n\nDate :- `{current_date}`\n\n👋 Your Paid Plan Has Expired On {will_expire}\n\n__**Plan 1**__\n\n`49/M\n\nAll Features Of This Bot`\n\n__**Plan 2**__\n\n`130 For 3 Month\n\nAll Features Of This Bot`\n\n__**Plan 2**__\n\n`500 For 1 Year\n\nAll Features Of This Bot`\n\n||**Need More Plans Contact To Our Developer :- @DKBOTZHELP**||",
            reply_markup=SUB_BUTTONS,
            disable_web_page_preview=True,
            quote=True,
        )
