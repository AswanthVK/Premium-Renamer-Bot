from .rename import queue
from ..config import Config
from ..tools.text import TEXT
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup 


@Client.on_message(filters.command("help") & filters.private & filters.incoming)
async def help(c, m, cb=False):
    
    if not await c.db.is_user_exist(m.from_user.id):
        await c.db.add_user(m.from_user.id)
        await c.send_message(
            Config.DB_CHANNEL_ID,
            f"New User {m.from_user.mention} started."
        )
    button = [[
        InlineKeyboardButton('🏕️ Home', callback_data='back'),
        InlineKeyboardButton('💸 Donate', callback_data='donate')
        ],[
        InlineKeyboardButton('❌ Close', callback_data='close')
    ]]
    reply_markup = InlineKeyboardMarkup(button)

    if cb:
        try:
            await m.message.edit(
                text=TEXT.HELP_USER.format(m.from_user.first_name),
                disable_web_page_preview=True,
                reply_markup=reply_markup
            )
        except:
            pass
    else:
        await m.reply_text(
            text=TEXT.HELP_USER.format(m.from_user.first_name),
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            quote=True
        )



@Client.on_message(filters.command("start") & filters.private & filters.incoming)
async def start(c, m, cb=False):
    if not await c.db.is_user_exist(m.from_user.id):
        await c.db.add_user(m.from_user.id)
        await c.send_message(
            Config.DB_CHANNEL_ID,
            f"New User {m.from_user.mention} started."
        )
    if not cb:
        start = await m.reply_text("**Checking...**", parse_mode="markdown", quote=True)

    button = [
        [
            InlineKeyboardButton('🧔 Developer', url='https://t.me/DKBOTZHELP'),
            InlineKeyboardButton('📘 About', callback_data='about')
        ],
        [
            InlineKeyboardButton('💡 Help', callback_data="help"),
            InlineKeyboardButton('🛠 Settings', callback_data="setting")
        ],
        [
            InlineKeyboardButton('❌ Close', callback_data="close")
        ],
    ]
    reply_markup = InlineKeyboardMarkup(button)
    if cb:
        try:
            await m.message.edit(
                text=TEXT.START_TEXT.format(m.from_user.first_name), 
                disable_web_page_preview=True,
                reply_markup=reply_markup
            )
        except:
            pass
    else:
        await start.edit(
            text=TEXT.START_TEXT.format(m.from_user.first_name), 
            disable_web_page_preview=True,
            reply_markup=reply_markup
        ) 


@Client.on_message(filters.command("about") & filters.private & filters.incoming)
async def about(c, m, cb=False):
    if not await c.db.is_user_exist(m.from_user.id):
        await c.db.add_user(m.from_user.id)
        await c.send_message(
            Config.DB_CHANNEL_ID,
            f"New User {m.from_user.mention} started."
        )
    restart_time = Config.RESTART_TIME[0]
    time_format = restart_time.strftime("%d %B %Y %I:%M %p")
    button = [[
        InlineKeyboardButton('🏕️ Home', callback_data='back'),
        InlineKeyboardButton('💸 Donate', callback_data='donate')
        ],[
        InlineKeyboardButton('❌ Close', callback_data='close')
    ]]
    reply_markup = InlineKeyboardMarkup(button)
    if cb:
        try:
            await m.message.edit(
                text=TEXT.ABOUT.format(time_format),
                disable_web_page_preview=True,
                reply_markup=reply_markup
            )
        except:
            pass
    else:
        await m.reply_text(
            text=TEXT.ABOUT.format(time_format),
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            quote=True
        )

@Client.on_message(filters.command("set_caption") & filters.private & filters.incoming)
async def set_caption(c, m):
    if not await c.db.is_user_exist(m.from_user.id):
        await c.db.add_user(m.from_user.id)

    buttons = [[
        InlineKeyboardButton('👀 Show Caption', callback_data='show_caption'),
        InlineKeyboardButton('❌ Close', callback_data='close')
    ]]

    if len(m.command) == 1:
        await m.reply_text(
            "⭐ Use this command to set the custom caption for your files. "
            "For setting your caption send caption in the format \n`/set_caption < your_caption >`\n\n"
            "--**Examples:**--\n\n**Simple caption:** `/set_caption My caption`\n\n"
            "**Dynamic capiton:**\n`/set_caption 📕 File Name: {filename}\n\n💾 Size: {filesize}\n\n⏰ Duration: {duration}`\n\n\n"
            "--**Available Variables:**--\n\n"
            "    • `{filename}` - replaced by the filename\n"
            "    • `{duration}` - replaced by the duration of videos\n"
            "    • `{filesize}` - replaced by filesize\n"
            "    • `{mimeType}` - replaced by the media mimeType\n"
            "    • `{caption}` - replaced with the previous file caption\n\n"
            "**Note:**\n1. You can check the current caption using /caption",
            reply_markup=InlineKeyboardMarkup(buttons),
            quote=True)
    else:
        if len(m.text.markdown) > len(m.text.html):
            caption = m.text.markdown.split(' ', 1)[1]
        else:
            caption = m.text.html.split(' ', 1)[1]
        await c.db.update_settings_status(m.from_user.id, 'custom_caption', caption)
        await m.reply_text(f'--**Your Caption:**--\n\n{caption}', reply_markup=InlineKeyboardMarkup(buttons), quote=True)


@Client.on_message(filters.command("caption") & filters.private & filters.incoming)
async def caption(c, m, cb=False):
    if not await c.db.is_user_exist(m.from_user.id):
        await c.db.add_user(m.from_user.id)

    caption = await c.db.get_settings_status(m.from_user.id, 'custom_caption')
    buttons = [[
        InlineKeyboardButton('💫 Refresh', callback_data='show_caption'),
        ],[
        InlineKeyboardButton('❌ Close', callback_data='close')
    ]]
    if not caption:
        text = "You didn't set any custom caption yet for setting custom caption use /set_caption 🔥."
    else:
        buttons[0].append(InlineKeyboardButton('🗑 Deleted Caption', callback_data='del_cap'))
        text = f"--**💬 Your custom caption:**-- \n\n{caption}"
    if cb:
        try:
           await m.answer()
           await m.message.edit(text, reply_markup=InlineKeyboardMarkup(buttons))
        except:
            pass
    else:
        await m.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons), quote=True)


@Client.on_message(filters.command("del_caption") & filters.private & filters.incoming)
async def delcap(c, m):
    if not await c.db.is_user_exist(m.from_user.id):
        await c.db.add_user(m.from_user.id)
    caption = await c.db.get_settings_status(m.from_user.id, 'custom_caption')
    if not caption:
        text = "__You didn't set any caption yet 😩__"
    else:
        await c.db.update_settings_status(m.from_user.id, 'custom_caption', '')
        text = "__Default caption deleted successfully ✨__"
    await m.reply_text(text, quote=True)


@Client.on_message(filters.command("warn"))
async def warn(c, m):
    if m.from_user.id in Config.AUTH_USERS:
        if len(m.command) >= 3:
            try:
                user_id = m.text.split(' ', 2)[1]
                reason = m.text.split(' ', 2)[2]
                await m.reply_text("User Notfied Sucessfully")
                await c.send_message(chat_id=int(user_id), text=reason)
            except:
                 await m.reply_text("User Not Notfied Sucessfully 😔")
    else:
        await m.reply_text(text="You Are Not Admin 😡", quote=True)


@Client.on_message(filters.command('list'))
async def list(c, m):
    result = queue._unfinished_tasks - len(queue._queue)
    await m.reply_text(f'**💥 Active Tasks:** {result}\n\n**🕐 Pending:** {len(queue._queue)}', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Close ❌', callback_data='close')]]), quote=True)
