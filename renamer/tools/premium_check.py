import logging
import time
import datetime
from ..config import Config
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserBannedInChannel, UserNotParticipant, MessageNotModified


logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

GB_USERS = []


async def premium_check(c, m, sent):
    """Checking the time gap is completed or not 
    and checking the parallel process"""

    try:
        chat = await c.get_chat_member('DKBOTZ', m.from_user.id)
        if chat.status=='kicked':
            await sent.edit('😡 You Are Banned 😝')
            return True

    except UserNotParticipant:
        button = [[InlineKeyboardButton('🔰 Join Now 🔰', url='https://t.me/DKBOTZ')]]
        markup = InlineKeyboardMarkup(button)
        await sent.edit(text=f"👋 Hi {m.from_user.mention(style='md')},\n\n**Please Join My Updates Channel to use this Bot!**\n\nDue to Overload, Only Channel Subscribers can use the Bot!", parse_mode='markdown', reply_markup=markup)
        return True

    except Exception as e:
        await sent.edit("**Something went Wrong. Contact my [Support Group](https://t.me/DKBOTZSUPPORT)**", disable_web_page_preview=True)
        return True

    if not await c.db.is_user_exist(m.from_user.id):
        await c.db.add_user(m.from_user.id)
        await c.send_message(
            Config.DB_CHANNEL_ID,
            f"New User {m.from_user.mention} started."
        )


   # Removed This Function Because This Bot For Premium Users

    #if m.from_user.id in Config.TIME_GAP1:
        # If one process is running
        #text = "**✋ Please wait untill the previous task complete.**\n\n"
        #text += "After previous task completed there will be a time gap.\n"
        #text += "__Time gap will be same as time consumed by your previous task ⏱.__"
        #await sent.edit(
            #text=text,
            #parse_mode="markdown"
        #)
        #return True




    #elif m.from_user.id in Config.TIME_GAP2:
        # if time gap not completed
        #msg = Config.timegap_message[m.from_user.id]
        #await sent.delete()
        #await msg.reply_text(
            #text="**👆 See this message and don't disturb me again 😏**",
            #parse_mode="markdown",
            #quote=True
        #)
        #return True

    SUB_BUTTONS = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Functions", callback_data="function"),
                InlineKeyboardButton("Instructions", callback_data="instruct"),
            ],
            [InlineKeyboardButton("Pay Now", url="https://te.legra.ph/Payment-07-06")],
        ]
    )
    user_id = m.from_user.id
    logger.info(
        f"👉 Sent A File 👈 By User {m.from_user.id} @{m.from_user.username}"
    )
    if Config.PAID_BOT.upper() == "YES":
        try:
            paid_status = await c.db.get_paid_status(user_id)
        except:
            await sent.edit(text="⚠️ First Click on /start, Then try again")
            return True
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
                    await sent.edit(
                        text=f"👋 Your paid plan has Expired on {will_expire}\n\nIf you want to use the bot, You can do so by Paying.",
                        parse_mode="markdown",
                        quote=True
                    )
                except Exception as e:
                    logger.info(f"⚠️ Error: {e}")
                for i in Config.AUTH_USERS:
                    try:
                        await c.send_message(
                            i,
                            text=f"🌟 **Plan Expired:** \n\n**User Id:** `{update.from_user.id}`\n\n**User Name:** @{update.from_user.username}\n\n**Plan Validity:** {paid_duration} Days\n\n**Joined On** : {paid_on}\n\n**Discription** : {paid_reason}",
                        )
                    except Exception:
                        logger.info(f"⚠️ Not found id {i}")
                return True

            else:
                pass

        else:
            await m.reply_text(
                text="Only paid users can use me. For more information Click on **Instructions** Buttons",
                reply_markup=SUB_BUTTONS,
                disable_web_page_preview=True,
                quote=True,
            )
            return True

    ban_status = await c.db.get_ban_status(m.from_user.id)
    if ban_status["is_banned"]:
        if (datetime.date.today() - datetime.date.fromisoformat(ban_status["banned_on"])).days > ban_status["ban_duration"]:
            await c.db.remove_ban(m.from_user.id)
        else:
            banned_text = "--**🛑 YOU ARE BANNED🛑**--\n\n"
            banned_text += '**Banned Date:** '
            banned_text += f"`{ban_status['banned_on']}`\n"
            banned_text += '**Banned Duration:** '
            banned_text += f"{ban_status['ban_duration']} day(s)\n"
            banned_text += '**Reason:** '
            banned_text += f"__**{ban_status['ban_reason']}**__\n\n"
            banned_text += f"if you think this is a mistake contact [𝐀𝐧𝐨𝐧𝐲𝐦𝐨𝐮𝐬](https://t.me/DKBOTZHELP)"
            await sent.edit(banned_text)
            await c.send_sticker(
                chat_id=m.chat.id,
                sticker="CAACAgEAAxkBAAECFrdhvdCWEWU-CLXsSot2Dizyn_FkNAAC7wEAAnzn8UWxlVoBHyE2gh4E",
            )
            return True  

    elif m.from_user.id in Config.TIME_GAP2:
        # if time gap not completed
        msg = Config.timegap_message[m.from_user.id]
        await sent.delete()
        await msg.reply_text(
            text="**👆 See This Message And don't disturb me again 😏**",
            parse_mode="markdown",
            quote=True
        )
        return True
    else:
        return False
