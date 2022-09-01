import logging
logger = logging.getLogger(__name__)

import os
import time
import shutil
import random
import asyncio
from .progress_bar import TimeFormatter
from .take_screen_shot import take_screen_shot
from .get_duration import get_duration


async def generate_sample(location, c, m):
      try:
          send_message = await m.reply_text(text="Trying to generate sample video 📹", quote=True)

          # creating output directory 
          output_directory = f"./DOWNLOADS/{m.from_user.id}/{time.time()}"
          if not os.path.isdir(output_directory):
              os.makedirs(output_directory)

          # trying to get duration if Failed sending error message
          duration = await get_duration(location)
          if isinstance(duration, str):
              return await send_message.edit("**Hey, i am unable to generate sample video 😑**")

          # getting the starting and ending time of video
          reduced_sec = duration - int(duration * 10 / 100)
          sample_duration = await c.db.get_settings_status(m.from_user.id, 'sample_video')

          # stopping process if duration is less than sample video duration 
          if sample_duration > reduced_sec:
              return await send_message.edit("😒 Sorry i can't generate sample beacuse this **video duration** is less than **sample video duration**")

          start = random.randint(0, reduced_sec - sample_duration)
          final_location = f"{output_directory}/sample video.mkv"

          # Trying to generate sample video if failes sending error message
          try:
              await send_message.edit("😎 **Generating Sample Video**")
          except:
              pass
          try:
              await trim_video(location, start, sample_duration, final_location)
              if (not os.path.exists(final_location)) or (os.path.getsize(final_location) == 0):
                  return await send_message.edit("**Unable to generate samplevideo 🤧**")
          except Exception as e:
              logger.warning(e)
              return await send_message.edit("**Unable to generate samplevideo 🤧**")

          await send_message.edit("**😤 Sample Video generated sucessfully.**\n\n__Now trying to upload__")
          duration = await get_duration(final_location)
          thumb_image_path = f"{output_directory}/{m.from_user.id}.jpg"
          try:
              thumb_image_path = await take_screen_shot(final_location, os.path.dirname(thumb_image_path), random.randint(0, duration - 1))
          except:
              thumb_image_path = None
          try:
              Video = await m.reply_video(
                  video=final_location,
                  duration=duration,
                  thumb=thumb_image_path,
                  caption=f"__sample video of {sample_duration}sec from {TimeFormatter(start)}__",
                  supports_streaming=True
              )
              await send_message.delete()
              if Video is None:
                  await send_message.edit("**Upload failed!!**")
          except Exception as e:
              await send_message.edit(f"**Unable to upload sample video!!**\n\nReason: {e}")
          try:
              os.remove(final_location)
          except:
              pass

      except Exception as e:
          print(e)
          await send_message.edit(f"**Failed to generate sample video!!**\n\nDue some programming error. Report this issue in [DK BOTZ SUPPORT](https://telegram.dog/DKBOTZSUPPORT)", parse_mode="markdown", disable_web_page_preview=True)


async def trim_video(location, start, sample_duration, final_location):
    subtitle_option = await fix_subtitle_codec(location)
    ffmpeg_cmd = ["ffmpeg", "-ss", str(start), "-i", location, "-t", str(sample_duration), "-map", "0",  "-c", "copy", final_location]
    for option in subtitle_option:
        ffmpeg_cmd.insert(-1, option)

    process = await asyncio.create_subprocess_exec(
        *ffmpeg_cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    await process.communicate()


async def fix_subtitle_codec(file):
    fixable_codecs = ["mov_text"]

    ffmpeg_dur_cmd = ["ffprobe", "-i", file, "-v", "error", "-select_streams", "s", "-show_entries", "stream=codec_name", "-of", "default=noprint_wrappers=1:nokey=1"]

    process = await asyncio.create_subprocess_exec(
        *ffmpeg_dur_cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    out, err = await process.communicate()
    out = out.decode().strip()
    if not out:
        return []

    fix_cmd = []
    codecs = [i.strip() for i in out.split("\n")]
    for indx, codec in enumerate(codecs):
        if any(fixable_codec in codec for fixable_codec in fixable_codecs):
            fix_cmd += [f"-c:s:{indx}", "srt"]

    return fix_cmd
