from aiogram import Bot, Dispatcher, executor, types
import config
import asyncio
import random
from aiogram.utils.executor import start_webhook

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, ParseMode

from aiogram.utils.markdown import link

import messages
import kb
import audio_id

#Запускаем трансформер
import transformer


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

buts0 = [
    KeyboardButton(kb.smile),
    KeyboardButton(kb.volunteer_on),
    KeyboardButton(kb.talk),
    KeyboardButton(kb.meditate),
    KeyboardButton(kb.call),
]

buts1 = [
    KeyboardButton(kb.smile),
    KeyboardButton(kb.volunteer_off),
    KeyboardButton(kb.talk),
    KeyboardButton(kb.meditate),
    KeyboardButton(kb.call),
]

global_key0 = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
)

for but in buts0:
    global_key0.add(but)

global_key1 = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
)

for but in buts1:
    global_key1.add(but)


def write_file():
    f = open('members.txt', 'w')
    for i in members:
        f.write(str(i) + '\n')
    f.close()


def read_file():
    f = open('members.txt', 'r')
    ans = [i[:-1] for i in f]
    f.close()

    return ans


members = read_file()


def true_kb(user_id):
    if user_id in members:
        return global_key1
    else:
        return global_key0

@dp.message_handler(commands=['start'])
async def start(msg):
    chat_id = msg.chat.id
    user_id = msg['from']['username']

    await bot.send_message(
        chat_id,
        messages.start,
        reply_markup=true_kb(user_id)
    )


@dp.message_handler(content_types=["text"])
async def main_logic(msg):
    chat_id = msg.chat.id
    user_id = msg['from']['username']

    if flag:
        answer = transformer.predict(msg.text)

        await bot.send_message(
            chat_id,
            answer
        )
        return

    if msg.text.lower() == 'стоп':
        flag = 0
        await bot.send_message(
            chat_id,
            'Режим чат бота выключен',
            reply_markup=true_kb(user_id)
        )
    elif msg.text == kb.smile:
        f = open('mems/' + str(random.randint(1, 5)) + '.jpg', 'rb')
        await bot.send_photo(
            chat_id,
            f,
            reply_markup=true_kb(user_id)
        )
    elif msg.text == kb.volunteer_on:
        if user_id in members:
            pass
        else:
            members.append(user_id)
            write_file()
            await bot.send_message(
                chat_id,
                'Отлично! Вы стали волонтером. Теперь люди, которым нужна помощь, могут обратиться к вам!',
                reply_markup=true_kb(user_id)
            )
    elif msg.text == kb.volunteer_off:
        if user_id in members:
            members.remove(user_id)
            write_file()
            await bot.send_message(
                chat_id,
                'Вы теперь не волонтер:(',
                reply_markup=true_kb(user_id)
            )
        else:
            pass
    elif msg.text == kb.talk:
        b0 = KeyboardButton(kb.talk_bot)
        b1 = KeyboardButton(kb.talk_man)

        key_talk = ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True
        ).add(b0).add(b1)

        await bot.send_message(
            chat_id,
            'С кем вы хотите поговорить?',
            reply_markup=key_talk
        )
    elif msg.text == kb.talk_bot:
        flag = 1
        await bot.send_message(
            chat_id,
            'Привет! Ты можешь поговорить со мной. Чтобы выключить режим чат-бота напишите слово СТОП'
        )

        '''
        await bot.send_message(
            chat_id,
            'Напиши моему другу @PMstudent_bot',
            reply_markup=true_kb(user_id)
        )
        '''
    elif msg.text == kb.talk_man:
        n = len(members)
        m = 'В данный момент волонтеров нет. Вы можете стать первым и помочь кому-то!'
        if n:
            mem = members[random.randint(0, n-1)]
            m = 'Напиши этому волонтеру @' + mem

        await bot.send_message(
            chat_id,
            m,
            reply_markup=true_kb(user_id)
        )
    elif msg.text == kb.meditate:
        #f = open('data/5.mp3', 'rb')
        msg = await bot.send_audio(
            chat_id,
            audio_id.audios[random.randint(1, 5)],
            reply_markup=true_kb(user_id)
        )
    elif msg.text == kb.call:
        await bot.send_message(
            chat_id,
            messages.call,
            reply_markup=true_kb(user_id),
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
