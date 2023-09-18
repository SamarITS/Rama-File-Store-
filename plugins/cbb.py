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
            text = f"""<b>🎧 𝐌𝐲 𝐍𝐚𝐦𝐞 𝐢𝐬 : <a href=https://t.me/SMD_New_Robot>🏞 𝐒𝐌𝐃 𝐅𝐈𝐋𝐄𝐒 𝐒𝐓𝐎𝐑𝐄 🎇</a>
😈 𝐀𝐫𝐭𝐢𝐬𝐭 : <a href=https://t.me/SMD_Owner>🍁𝐂𝐨𝐝𝐞𝐫🎎</a>
👑 𝐃𝐞𝐯𝐨𝐥𝐨𝐩𝐞𝐫 : <a href=https://t.me/SMD_Owner>🌿𝐌𝐚𝐤𝐞𝐫⚜️</a>
✍️ 𝐆𝐫𝐚𝐝𝐮𝐚𝐭𝐞 : <a href=https://t.me/SMD_Owner>🛬 𝐏𝐫𝐨𝐝𝐮𝐜𝐞𝐫🚦</a>
♠ 𝐊𝐨𝐥𝐚𝐫𝐮 : <a href=https://t.me/SMD_Owner>🎭𝐒𝐫𝐞𝐞𝐫𝐚𝐚𝐦🔥</a>
👨‍🔧 𝐇𝐞𝐥𝐩𝐞𝐫 : <a href=https://t.me/SMD_Owner>🦞𝐑𝐚𝐚𝐦🌿</a>
⚜️ 𝐒𝐌𝐃 𝐁𝐎𝐓𝐳 : <a href=https://t.me/QTVS_BOT_X_CLOUD>🥀𝐌𝐂𝐔🎋</a></b>""",
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
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
