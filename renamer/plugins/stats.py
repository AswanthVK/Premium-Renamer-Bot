import logging

logger = logging.getLogger(__name__)

import shutil
from os import execl
from sys import executable
from time import sleep, time

from psutil import Process as psprocess
from psutil import (
    cpu_count,
    cpu_percent,
    disk_usage,
    net_io_counters,
    swap_memory,
    virtual_memory,
)
from pyrogram import Client, enums, filters
from pyrogram.errors import FloodWait, RPCError

from ..config import Config


SIZE_UNITS = ["B", "KB", "MB", "GB", "TB", "PB"]


def get_readable_file_size(size_in_bytes) -> str:
    if size_in_bytes is None:
        return "0B"
    index = 0
    while size_in_bytes >= 1024:
        size_in_bytes /= 1024
        index += 1
    try:
        return f"{round(size_in_bytes, 2)}{SIZE_UNITS[index]}"
    except IndexError:
        return "File too large"


def get_readable_time(seconds: int) -> str:
    result = ""
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
    if days != 0:
        result += f"{days}d "
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f"{hours}h "
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f"{minutes}m "
    seconds = int(seconds)
    result += f"{seconds}s"
    return result


@Client.on_message(filters.command(["stats"]) & filters.user(Config.AUTH_USERS))
async def statuss_(bot, update):
    currentTime = get_readable_time(time() - Start_Time)
    total, used, free, disk = disk_usage("/")
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)
    sent = get_readable_file_size(net_io_counters().bytes_sent)
    recv = get_readable_file_size(net_io_counters().bytes_recv)
    cpuUsage = cpu_percent(interval=0.5)
    p_core = cpu_count(logical=False)
    t_core = cpu_count(logical=True)
    swap = swap_memory()
    swap_p = swap.percent
    swap_t = get_readable_file_size(swap.total)
    get_readable_file_size(swap.used)
    memory = virtual_memory()
    mem_p = memory.percent
    mem_t = get_readable_file_size(memory.total)
    mem_a = get_readable_file_size(memory.available)
    mem_u = get_readable_file_size(memory.used)
    stats = (
        f"**Bot Uptime:** {currentTime}\n\n"
        f"**Total Disk Space:** {total}\n"
        f"**Used:** {used} | **Free:** {free}\n\n"
        f"**Upload:** {sent}\n"
        f"**Download:** {recv}\n\n"
        f"**CPU:** {cpuUsage}%\n"
        f"**RAM:** {mem_p}%\n"
        f"**DISK:** {disk}%\n\n"
        f"**Physical Cores:** {p_core}\n"
        f"**Total Cores:** {t_core}\n\n"
        f"**SWAP:** {swap_t} | **Used:** {swap_p}%\n"
        f"**Memory Total:** {mem_t}\n"
        f"**Memory Free:** {mem_a}\n"
        f"**Memory Used:** {mem_u}\n"
    )
    try:
        await update.reply_text(f"{stats}", reply_to_message_id=update.id)
    except Exception as e:
        print(e)



@Client.on_message(filters.command(["restart"]) & filters.user(Config.AUTH_USERS))
async def bot_restart(bot, update):

    try:
        await update.reply_text("**♻️ Restarted Successfully **")
    except:
        pass

    try:
        shutil.rmtree(Config.DOWNLOAD_PATH)
        logger.info("Deleted DOWNLOAD_PATH successfully ✅")
    except:
        pass

    try:
        procs = psprocess(worker.pid)
        for proc in procs.children(recursive=True):
            proc.kill()
        procs.kill()
    except Exception as e:
        print(e)

    try:
        logger.info(
            f"{update.from_user.id} {update.from_user.first_name} : Restarting..."
        )
        execl(executable, executable, "run_clients.py")
    except Exception as e:
        print(e)
