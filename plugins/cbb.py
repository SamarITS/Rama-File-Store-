#(©)MR-X-MIRROR-BOTZ

from pyrogram import __version__
from bot import Bot
from config import OWNER_ID
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text =f"""<b>
╭────[ About Page ]────⍟
│
├⍟ Meh Name : <a href=http://t.me/Datas_StoreBot><b>𝐅𝐢𝐥𝐞𝐒𝐭𝐨𝐫𝐞 𝐁𝐨𝐭</b></a>
├⍟ Owner : <a href=https://t.me/SMD_Owner><b>𝐒𝐌𝐃</b></a>
├⍟ Version : SMD 1.0 [ Stable ]
├⍟ Server : Koyeb
├⍟ Language : Python 3.10.8
├⍟ Framework : Pyrogram 2.0.97
├⍟ Developer : <a href=https://t.me/SMD_Owner><b>𝐒𝐌𝐃 𝐁𝐎𝐓𝐳</b></a>
├⍟ Powered By  : <a href=https://t.me/SMD_BOTz><b>BOT Update</b></a>
│
╰────[ <a href=https://t.me/SMD_Owner><b>𝐒𝐌𝐃 𝐁𝐎𝐓𝐳</b></a> ]────⍟<b>""",
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("✨ Update", url = "https://t.me/SMD_BOTz")
                        InlineKeyboardButton("🎋 About", callback_data = "about")
                        InlineKeyboardButton("👑 Home", callback_data = "Start")
                        InlineKeyboardButton("🔒 Close", callback_data = "close")
                    ]
                ]
            )
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
