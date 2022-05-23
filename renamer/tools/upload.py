import asyncio
from pyrogram.errors import FloodWait 
from .progress_bar import progress_bar


async def upload_video(c, m, new_file_name, final_caption, duration, width, height, thumbnail, start_time, msg, id):
    try:
        final_media = await m.reply_video(
            video=new_file_name,
            caption=final_caption,
            duration=duration,
            width=width,
            height=height,
            supports_streaming=True,
            thumb=thumbnail,
            quote=True,
            progress=progress_bar,
            progress_args=("Upload Status:", start_time, c, msg, id, 'video')
        )
        return final_media
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await upload_video(c, m, new_file_name, final_caption, duration, width, height, thumbnail, start_time, msg, id)
    except Exception as e:
        await msg.edit(f"--Error:--\n{e}") 
        return False


async def upload_file(c, m, new_file_name, thumbnail, final_caption, start_time, msg, id):
    try:
        final_media = await m.reply_document(
            document=new_file_name,
            thumb=thumbnail,
            force_document=True,
            caption=final_caption,
            quote=True,
            progress=progress_bar,
            progress_args=("Upload Status:", start_time, c, msg, id, 'document')  
        )
        return final_media
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await upload_file(c, m, new_file_name, thumbnail, final_caption, start_time, msg, id)
    except Exception as e:
        await msg.edit(f"--Error:--\n{e}")
        return False


async def upload_photo(c, m, new_file_name, final_caption, start_time, msg, id):
    try:
        final_media = await m.reply_photo(
            photo=new_file_name,
            caption=final_caption,
            quote=True,
            progress=progress_bar,
            progress_args=("Upload Status:", start_time, c, msg, id, 'photo')  
        )
        return final_media
    except FloodWait:
        await asyncio.sleep(e.x)
        await upload_photo(c, m, new_file_name, final_caption, start_time, msg, id)
    except Exception as e:
        await msg.edit(f"--Error:--\n{e}")
        return False 


async def upload_audio(c, m, new_file_name, duration, thumbnail, final_caption, start_time, msg, id):
    try:
        await m.reply_audio(
            audio=new_file_name,
            caption=final_caption,
            duration=duration,
            thumb=thumbnail,
            quote=True,
            progress=progress_bar,
            progress_args=("Upload Status:", start_time, c, msg, id, 'audio')  
        )
    except FloodWait:
        await asyncio.sleep(e.x)
        await upload_audio(c, m, new_file_name, duration, thumbnail, final_caption, start_time, msg, id)
    except Exception as e:
        await msg.edit(f"--Error:--\n{e}")
        return False 
