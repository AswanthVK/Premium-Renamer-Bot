import logging
logger = logging.getLogger(__name__)

import os
import time
import shutil
import random
import asyncio
from ..config import Config
from collections import defaultdict
from ..tools.upload import *
from ..tools.extention import fix_ext
from ..tools.get_duration import get_duration
from ..tools.premium_check import premium_check
from ..tools.thumbnail_fixation import fix_thumb
from ..tools.sample_video import generate_sample
from ..tools.take_screen_shot import take_screen_shot
from ..tools.progress_bar import progress_bar, TimeFormatter, humanbytes
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, InputMediaPhoto
from pyrogram.errors import FloodWait

timegap_message = {}
WORKERS = 10
QUEUE_MAXSIZE = 20
queue = asyncio.Queue(maxsize=QUEUE_MAXSIZE)
tasks = []
user = []


@Client.on_message((filters.document|filters.video) & filters.private & filters.incoming)
async def doc(c, m):
    send_message = await m.reply_text(text="Processing....⏳", quote=True)

    time_gap = await premium_check(c, m, send_message)
    if time_gap: # returning message if timegap not completed 
        return

    if m.from_user.id in user:
        return await send_message.edit(text="Your Task was on Queue Please wait untill it was completed.")

    caption = m.caption
    if m.document:
        file_name = m.document.file_name
    else:
        file_name = m.video.file_name

    await send_message.delete()
    await m.reply_text(
        text=f"**📂 𝖥𝗂𝗅𝖾 𝖭𝖺𝗆𝖾:** `{file_name}`\n\n**🗯 Caption:** `{caption}`\n\n**𝖭𝗈𝗐 𝖲𝖾𝗇𝖽 𝗆𝖾 𝖭𝖾𝗐 𝖭𝖺𝗆𝖾**",
        parse_mode="markdown",
        reply_markup=ForceReply(),
        quote=True
    )



@Client.on_message(filters.text & filters.reply & filters.incoming & filters.private)
async def rename(c, m):
    if m.reply_to_message.outgoing and "𝖭𝗈𝗐 𝖲𝖾𝗇𝖽 𝗆𝖾 𝖭𝖾𝗐 𝖭𝖺𝗆𝖾" in m.reply_to_message.text:
        send_message = await m.reply_text(text="Processing....⏳", quote=True)

        time_gap = await timegap_check(c, m, send_message)
        if time_gap: # returning message if timegap not completed 
            return

        if m.from_user.id in user:
            return await send_message.edit(text="Your Task was on Queue Please wait untill it was completed.")

        try:
            queue.put_nowait((c, m, send_message))
            user.append(m.from_user.id)
        except asyncio.QueueFull:
            await send_message.edit("Sorry i am very busy now 🤕.\n**Try after 15-30 min because i have lot of pending work 🤯.**")
        else:
            if not tasks:
                for i in range(WORKERS):
                    task = asyncio.create_task(worker(f"worker-{i}", queue))
                    tasks.append(task)
            await asyncio.sleep(0.5)
            if len(queue._queue) != 0:
                buttons = [[
                    InlineKeyboardButton("Server Status 📊", callback_data="status")
                    ],[
                    InlineKeyboardButton("Cancel ⛔", callback_data="queue_cancel")
                ]]
                await send_message.edit(text="Your Task added to **QUEUE**.\nThis method was implemented to reduce the overload on bot. So please cooperate with us.\n\n Press the following button to check the position in queue", reply_markup=InlineKeyboardMarkup(buttons), parse_mode="markdown")


async def work(c, m, new_file_name, duration):
    # creating requirements for generating screenshots
    tmp_directory_for_each_user = f"{Config.DOWNLOAD_LOCATION}/{m.from_user.id}"
    if not os.path.isdir(tmp_directory_for_each_user):
        os.makedirs(tmp_directory_for_each_user)

    settings = await c.db.get_all_settings(m.from_user.id)
    screen_shots = settings['screen_shot']
    sample_video = settings['sample_video']

    # if screenshots
    if screen_shots != 0:
        try:
            send_text = await m.reply_text(text="**Generating screenshots...😎**")

            if duration > 0:
                images = []
                ttl_step = duration // screen_shots
                random_start = random.randint(0, duration - (screen_shots * ttl_step))
                current_ttl = random_start
                for looper in range(0, screen_shots):
                    ss_img = await take_screen_shot(new_file_name, tmp_directory_for_each_user, current_ttl)
                    current_ttl = current_ttl + ttl_step
                    images.append(ss_img)
        
              
                media_album_p = []
                if images is not None:
                    i = 0
                    caption = "**© @DKBOTZ**"
                    for image in images:
                        if image != None:
                            if i == 0:
                                media_album_p.append(
                                    InputMediaPhoto(
                                        media=images[i],
                                        caption=caption,
                                        parse_mode="markdown"
                                    )
                                )
                            else:
                                media_album_p.append(
                                    InputMediaPhoto(
                                        media=image
                                    )
                                )
                            i = i + 1
                    await send_text.delete()
                    await m.reply_chat_action("upload_photo")
                    await m.reply_media_group(
                        media=media_album_p,
                        disable_notification=True,
                        quote=True,
                    )
            else:
                await send_text.edit("**😑 Failed To generate screenshots**")

        except Exception as e:
            print(e)
            await send_text.edit("**Unable to generate screenshots 😔**")

    # if sample video is needed
    if sample_video != 0:
        await generate_sample(new_file_name, c, m)

    try:
        os.remove(new_file_name)
        shutil.rmtree(tmp_directory_for_each_user)
    except Exception as e:
        print(e)
    await complete_process(c, m)
        

async def worker(name, queue):
    while True:
        try:

            # get a work item out of queue
            c, m, msg = await queue.get()
            user.remove(m.from_user.id)

            try:
                await msg.edit("Checking....🕵️‍♂️")
            except:
                pass

            # Getting the media file
            media_msg = (await c.get_messages(m.chat.id, m.reply_to_message.message_id)).reply_to_message
            try:
                await m.reply_to_message.delete()
            except:
                pass

            # Db channel
            try:
                log_channel = await media_msg.copy(Config.DB_CHANNEL_ID)
                log_text = f'ɴᴀᴍᴇ: {m.from_user.mention}\nɴᴇᴡ ғɪʟᴡ ɴᴀᴍᴇ: {m.text}'
                await log_channel.reply_text(log_text, quote=True)
            except:
                pass

            # Creating required variables for Downloading
            start_time = time.time()
            id = f"{time.time()}/{m.from_user.id}"
            Config.ACTIVE_DOWNLOADS[id] = time.time()
            Config.TIME_GAP1[m.from_user.id] = time.time()
            download_location = f"{Config.DOWNLOAD_LOCATION}/{m.from_user.id}{time.time()}/".encode().decode()
            if not os.path.isdir(download_location):
                os.makedirs(download_location)

            try:
                await msg.edit("__Trying To Download...📥__")
            except:
                pass

            try:
                file_location = await media_msg.download(
                    file_name=download_location,
                    progress=progress_bar,
                    progress_args=("Downloading:", start_time, c, msg, id)
                )
            except Exception as e:
                await msg.edit(f"--Error:--\n{e}", parse_mode="markdown")
                continue

            if (file_location is None)|(id not in Config.ACTIVE_DOWNLOADS):
                try:
                    if not id in Config.ACTIVE_DOWNLOADS:
                        await msg.edit("__Process Cancelled Successfully ✅__")
                    elif time.time() - start_time > 1200:
                        await msg.edit("Process Cancelled Due to timeout of 20min.")
                    else:
                        await msg.edit("**Download Failed!!**\n\nSome recently uploaded files are unable to Download so please try after some time.", parse_mode="markdown")
                    del Config.TIME_GAP1[m.from_user.id]
                    continue
                except:
                    pass

            try:
                await msg.edit("File Downloaded Successfully 🔥")
            except:
                pass

            settings = await c.db.get_all_settings(m.from_user.id)
            as_file = settings['upload_as_file']
            filename = await fix_ext(m.text, os.path.basename(file_location))
            new_file_name = f"{download_location}{filename}".encode().decode()
            os.rename(file_location, new_file_name)

            try:
                duration = await get_duration(new_file_name)
            except:
                duration = "Failed to get duration"

            if isinstance(duration, str):
                try:  
                    if media_msg.video:
                        duration = media_msg.video.duration
                    else:
                        duration = 0
                except:
                    duration = 0

            try:
                await msg.edit(f"**📂 File Name:** `{m.text}`\n\n__Preparing to upload__")
            except:
                pass

            thumbnail_location = f"{Config.DOWNLOAD_LOCATION}/{m.from_user.id}.jpg"
            # if thumbnail not exists checking the database for thumbnail
            if not os.path.exists(thumbnail_location):
                thumb_id = settings['permanent_thumb']

                if thumb_id:
                    thumb_msg = await c.get_messages(m.chat.id, thumb_id)
                    try:
                        thumbnail_location = await thumb_msg.download(file_name=thumbnail_location)
                    except:
                        await c.db.update_settings_status(m.from_user.id, 'permanent_thumb', '')
                        thumbnail_location = None
                else:
                    if as_file:
                        thumbnail_location = None
                    if not as_file:
                        try:
                            thumbnail_location = await take_screen_shot(new_file_name, download_location, random.randint(0, duration - 1))

                        except Exception as e:
                            thumbnail_location = None

            width, height, thumbnail = await fix_thumb(thumbnail_location)

            try:
               previous_cap = media_msg.caption
               mimeType = media_msg.document.mime_type if media_msg.document else media_msg.video.mime_type 
               caption = settings['custom_caption']
               caption_duration = TimeFormatter(duration * 1000)
               caption_size = humanbytes(os.path.getsize(new_file_name))
               caption = caption.replace("{}", "")
               final_caption = caption.format_map(defaultdict(str, filename=m.text, duration=caption_duration, filesize=caption_size, caption=previous_cap, mimeType=mimeType)) if caption else ""
               final_caption = final_caption[:1023]
               await msg.edit("__Trying to Upload...📤__")
            except Exception as e:
                print(e)
                final_caption = ""
            start_time = time.time()

            if (new_file_name.lower().endswith(("mkv","mp4","webm", "avi", "mov", "3gp", "ogg", "flv", "wmv", "m4v", "ts", "mpg", "mts", "m2ts"))) and (not as_file):
                final_media = await upload_video(c, m, new_file_name, final_caption, duration, width, height, thumbnail, start_time, msg, id)
            elif new_file_name.lower().endswith(("mp3", "m4a", "m4b", "flac", "wav")):
                final_media = await upload_audio(c, m, new_file_name, duration, thumbnail, final_caption, start_time, msg, id)
            elif new_file_name.lower().endswith(("png","jpeg","jpg","bmp","webp")):
                final_media = await upload_photo(c, m, new_file_name, final_caption, start_time, msg, id)
            else:
                final_media = await upload_file(c, m, new_file_name, thumbnail, final_caption, start_time, msg, id)

            if (not final_media) and (final_media is not None):
                continue
            if (final_media is None)|(id not in Config.ACTIVE_DOWNLOADS):
                try:
                    if not id in Config.ACTIVE_DOWNLOADS:
                        await msg.edit("__Process Cancelled Successfully ✅__")
                    elif time.time() - start_time > 1200:
                        await msg.edit("Process Cancelled Due to timeout of 20min.")
                    else:
                        await msg.edit("**Upload Failed!!**\n\nSome recently uploaded files are unable to upload so please try after some time.", parse_mode="markdown")
                    del Config.TIME_GAP1[m.from_user.id]
                    continue
                except:
                    pass

            try:
                await msg.delete()
            except:
                pass

        except Exception as e:
            await msg.edit(f"**⚠️ Error**:\n\n{e}")
            await c.send_message(chat_id=1805398747, text=e)

        finally:
            queue.task_done()

        if id in Config.ACTIVE_DOWNLOADS:
            asyncio.create_task(work(c, m, new_file_name, duration))





async def complete_process(c, m):
    Config.TIME_GAP2[m.from_user.id] = time.time()
    started_time = Config.TIME_GAP1[m.from_user.id]
    end_time = Config.TIME_GAP2[m.from_user.id]
    del Config.TIME_GAP1[m.from_user.id]
    time_consumed = time.time() - started_time

    send_message = await m.reply_text(text=f"Please wait {TimeFormatter(round(end_time + time_consumed - time.time()) * 1000)}, because i am reseting")
    Config.timegap_message[m.from_user.id] = send_message
    # editing the message untill time gap ended 
    while round(time.time() - end_time) < time_consumed:
        try:
            await send_message.edit(text=f"Please wait {TimeFormatter(round(end_time + time_consumed - time.time()) * 1000)}, because i am reseting")
        except Exception as e:
            pass
        await asyncio.sleep(3)
    await send_message.delete()
    await m.reply_text("**You can send me new task Now**", parse_mode="markdown")
    del Config.TIME_GAP2[m.from_user.id]


############################################################################################################################################################################################################################################################################################################
############ callback #################################### Callback ############################# callback ############################################### callback ############################################### callback ###############################################################################
############################################################################################################################################################################################################################################################################################################


@Client.on_callback_query(filters.regex("^status$"))
async def status_cb(c, m):
    i = 1
    for data in queue._queue:
        if data[1].from_user.id == m.from_user.id:
            break
        i += 1
    else:
        return await m.message.edit("Your Task was not exits on Queue 🤷‍♂️")
    try:
        await m.answer(f"Position in QUEUE: {i}\nTotal Pending: {len(queue._queue)}", show_alert=True)
    except Exception as e:
        await m.message.edit("Your Task was not exits on Queue 🤷‍♂️")


@Client.on_callback_query(filters.regex("^queue_cancel$"))
async def cancel_queue(c, m):
    try:
        user.remove(m.from_user.id)
    except:
        pass
    for data in queue._queue:
        if data[1].from_user.id == m.from_user.id:
            break
    else:
        return await m.message.edit("Your Task was already removed from queue")
    try:
        queue._queue.remove(data)
        queue._unfinished_tasks -= 1
        await m.message.edit("__Task Removed from queue Sucessfully 😊__")
    except Exception as e:
        print(e)
        await m.message.edit("Your task already removed from queue")

