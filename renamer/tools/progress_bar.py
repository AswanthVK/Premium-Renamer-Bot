import logging
logger = logging.getLogger(__name__)

import math
import time
import asyncio
from ..config import Config
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


############################# Progress Bar 📊 #############################

async def progress_bar(current, total, status_msg, start, c, m, id, sts=None):
    present = time.time()
    if (id in Config.ACTIVE_DOWNLOADS) & (present - start < 1200):
        if present - Config.ACTIVE_DOWNLOADS[id] > 5:
            if sts:
                try:
                    if sts == 'document':
                        await m.reply_chat_action('upload_document')
                    if sts == 'photo':
                        await m.reply_chat_action('upload_photo')
                    if sts == 'video':
                        await m.reply_chat_action('upload_video')
                    if sts == 'audio':
                        await m.reply_chat_action('upload_audio')
                except:
                    pass
            speed = current / (present - start)
            percentage = current * 100 / total
            time_to_complete = round(((total - current) / speed)) * 1000
            time_to_complete = TimeFormatter(time_to_complete)
            progressbar = "[{0}{1}]".format(\
                ''.join(["■" for i in range(math.floor(percentage / 10))]),
                ''.join(["□" for i in range(10 - math.floor(percentage / 10))])
                )
            current_message = f"**{status_msg}** {round(percentage, 2)}%\n\n{progressbar}\n\n🚀 **Speed**: {humanbytes(speed)}/sec\n\n✅ **Done**: {humanbytes(current)}\n\n🔰 **Size**: {humanbytes(total)}\n\n⏰ **Time Left**: {time_to_complete if round(start - present) != 0 else 'Calculating.....'}"
            try:
                button = [[InlineKeyboardButton("𝖢𝖠𝖭𝖢𝖤𝖫 ⛔", callback_data=f"cancel_download+{id}")]]
                await m.edit(
                    text=current_message,
                    parse_mode="markdown",
                    reply_markup=InlineKeyboardMarkup(button)
                )
                Config.ACTIVE_DOWNLOADS[id] = time.time()
            except:
                pass
    else:
        await c.stop_transmission()


############################# Size #############################

def humanbytes(size):
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'


############################# Time Formating ⏰ #############################

def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + " days, ") if days else "") + \
        ((str(hours) + " hrs, ") if hours else "") + \
        ((str(minutes) + " min, ") if minutes else "") + \
        ((str(seconds) + " sec, ") if seconds else "") + \
        ((str(milliseconds) + " millisec, ") if milliseconds else "")
    tmp = tmp[:-2] if tmp[:-2] != "" else 0
    return tmp


############################# END 🌋 #############################
