from aiogram import Bot, Dispatcher, executor, types
import config
import asyncio
from aiogram.utils.executor import start_webhook

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, ParseMode

from aiogram.utils.markdown import link


import messages
import kb


WEBHOOK_HOST = 'https://romanychev.online'
WEBHOOK_PATH = '/tasks/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '127.0.0.1'
WEBAPP_PORT = 7771

bot = Bot(token=config.token)
dp = Dispatcher(bot)


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    await bot.delete_webhook()

buts = [
    KeyboardButton(kb.smile),
    KeyboardButton(kb.volunteer),
    KeyboardButton(kb.talk),
    KeyboardButton(kb.meditate),
    KeyboardButton(kb.call),
]

global_key = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
)

for but in buts:
    global_key.add(but)


@dp.message_handler(commands=['start'])
async def start(msg):
    chat_id = msg.chat.id
    await bot.send_message(
        chat_id,
        messages.start,
        reply_markup=global_key
    )

@dp.message_handler(content_types=["text"])
async def main_logic(msg):
    chat_id = msg.chat.id

    if msg.text == kb.smile:
        pass
    elif msg.text == kb.volunteer:
        pass
    elif msg.text == kb.talk:
        await bot.send_message(
            chat_id,
            '@PMstudent_bot',
            reply_markup=global_key
        )
    elif msg.text == kb.meditate:
        pass
    elif msg.text == kb.call:
        await bot.send_message(
            chat_id,
            messages.call,
            reply_markup=global_key,
            parse_mode=ParseMode.MARKDOWN
        )


start_webhook(
    dispatcher=dp,
    webhook_path=WEBHOOK_PATH,
    on_startup=on_startup,
    on_shutdown=on_shutdown,
    skip_updates=True,
    host=WEBAPP_HOST,
    port=WEBAPP_PORT,
)
