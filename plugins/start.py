import os
import asyncio
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import ADMINS, FORCE_MSG, START_MSG, START_PIC, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT
from helper_func import subscribed, encode, decode, get_messages
from database.database import add_user, del_user, full_userbase, present_user


@Bot.on_message(filters.command('start') & filters.private)
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id
    if not await present_user(user_id):
        try:
            await add_user(user_id)
        except Exception as e:
            print(f"Error adding user: {e}")

    if len(message.text) > 7:
        try:
            base64_string = message.text.split(" ", 1)[1]
            decoded_string = await decode(base64_string)
            arguments = decoded_string.split("-")
        except Exception as e:
            print(f"Error decoding string: {e}")
            return

        try:
            if len(arguments) == 3:
                start = int(int(arguments[1]) / abs(client.db_channel.id))
                end = int(int(arguments[2]) / abs(client.db_channel.id))
                message_ids = range(start, end + 1) if start <= end else list(range(start, end - 1, -1))
            elif len(arguments) == 2:
                message_ids = [int(int(arguments[1]) / abs(client.db_channel.id))]
            else:
                return
        except ValueError as e:
            print(f"Error parsing IDs: {e}")
            return

        temp_msg = await message.reply("Please wait...")
        try:
            messages = await get_messages(client, message_ids)
        except Exception as e:
            await temp_msg.edit("Something went wrong!")
            print(f"Error fetching messages: {e}")
            return

        await temp_msg.delete()

        for msg in messages:
            caption = (
                CUSTOM_CAPTION.format(
                    previouscaption=msg.caption.html if msg.caption else "",
                    filename=msg.document.file_name
                )
                if CUSTOM_CAPTION and msg.document else msg.caption.html or ""
            )

            try:
                await msg.copy(
                    chat_id=user_id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=None if DISABLE_CHANNEL_BUTTON else msg.reply_markup,
                    protect_content=PROTECT_CONTENT
                )
                await asyncio.sleep(0.5)
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except Exception as e:
                print(f"Error copying message: {e}")
    else:
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("About", callback_data="about"),
             InlineKeyboardButton("🔒 Close", callback_data="close")]
        ])

        if START_PIC:
            await message.reply_photo(
                photo=START_PIC,
                caption=START_MSG.format(
                    first=message.from_user.first_name,
                    last=message.from_user.last_name,
                    username=f"@{message.from_user.username}" if message.from_user.username else "N/A",
                    mention=message.from_user.mention,
                    id=user_id
                ),
                reply_markup=reply_markup,
                quote=True
            )
        else:
            await message.reply_text(
                text=START_MSG.format(
                    first=message.from_user.first_name,
                    last=message.from_user.last_name,
                    username=f"@{message.from_user.username}" if message.from_user.username else "N/A",
                    mention=message.from_user.mention,
                    id=user_id
                ),
                reply_markup=reply_markup,
                disable_web_page_preview=True,
                quote=True
            )


@Bot.on_message(filters.command('start') & filters.private & ~filters.create(subscribed))
async def not_joined(client: Client, message: Message):
    buttons = [
        [InlineKeyboardButton("Join Channel", url=client.invitelink)],
        [InlineKeyboardButton("Try Again", url=f"https://t.me/{client.username}?start={message.command[1]}")] if len(message.command) > 1 else []
    ]

    await message.reply(
        text=FORCE_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username=f"@{message.from_user.username}" if message.from_user.username else "N/A",
            mention=message.from_user.mention,
            id=message.from_user.id
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True,
        quote=True
    )


@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    users = await full_userbase()
    await message.reply(f"{len(users)} users are using this bot")


@Bot.on_message(filters.command('broadcast') & filters.private & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if not message.reply_to_message:
        await message.reply("<code>Reply to a message to broadcast it.</code>")
        return

    users = await full_userbase()
    total, successful, blocked, deleted, unsuccessful = 0, 0, 0, 0, 0

    await message.reply("Broadcasting... This may take a while.")
    for user_id in users:
        try:
            await message.reply_to_message.copy(chat_id=user_id)
            successful += 1
        except FloodWait as e:
            await asyncio.sleep(e.x)
            successful += 1
        except UserIsBlocked:
            await del_user(user_id)
            blocked += 1
        except InputUserDeactivated:
            await del_user(user_id)
            deleted += 1
        except Exception:
            unsuccessful += 1
        total += 1

    status = (
        f"<b>Broadcast Completed</b>\n\n"
        f"Total Users: {total}\n"
        f"Successful: {successful}\n"
        f"Blocked: {blocked}\n"
        f"Deleted Accounts: {deleted}\n"
        f"Unsuccessful: {unsuccessful}"
    )
    await message.reply(status)
