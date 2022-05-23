from .commands import *
from ..config import Config
from ..tools.text import TEXT
from .commands import caption
from .thumbnail import delete_thumbnail
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserBannedInChannel, UserNotParticipant


@Client.on_callback_query(filters.regex('^help$'))
async def help_cb(c, m):
    await m.answer()
    await help(c, m, True)


@Client.on_callback_query(filters.regex('^donate$'))
async def donate(c, m):
    button = [[
        InlineKeyboardButton('🏕️ Home', callback_data='back'),
        InlineKeyboardButton('📘 About', callback_data='about')
        ],[
        InlineKeyboardButton('❌ Close', callback_data='close')
    ]]
    reply_markup = InlineKeyboardMarkup(button)
    await m.answer()
    await m.message.edit(
        text=TEXT.DONATE_USER.format(m.from_user.first_name),
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )


@Client.on_callback_query(filters.regex('^close$'))
async def close_cb(c, m):
    try:
        await m.message.delete()
        await m.message.reply_to_message.delete()
    except:
        pass


@Client.on_callback_query(filters.regex('^back$'))
async def back_cb(c, m):
    await m.answer()
    await start(c, m, True)


@Client.on_callback_query(filters.regex('^about$'))
async def about_cb(c, m):
    await m.answer()
    await about(c, m, True)
                

@Client.on_callback_query(filters.regex('^cancel_download\+'))
async def cancel_cb(c, m):
    await m.answer()
    await m.reply_chat_action("cancel")
    await m.message.edit(text="__🛠 Trying to Cancel__")
    id = m.data.split("+", 1)[1]
    if id not in Config.ACTIVE_DOWNLOADS:
        await m.message.edit("👁‍🗨 This process already cancelled,\n**Reason may be bot restarted**")
        return
    del Config.ACTIVE_DOWNLOADS[id]


@Client.on_callback_query(filters.regex('^del_cap$'))
async def del_cap(c, m):
    await c.db.update_settings_status(m.from_user.id, 'custom_caption', '')
    await caption(c, m, cb=True)


@Client.on_callback_query(filters.regex('^show_caption$'))
async def show_caption(c, m):
    await caption(c, m, cb=True)


@Client.on_callback_query(filters.regex('^del$'))
async def deletethumb_cb(c, m):
    await m.answer()
    await delete_thumbnail(c, m.message.reply_to_message)
    await m.message.delete()
