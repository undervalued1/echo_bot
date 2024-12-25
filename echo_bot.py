import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
import xml.etree.ElementTree as ET
import urllib.request

API_TOKEN = '7827869913:AAGusRIZjf41FPn7m0OezpRj_f73HssDjFg'

# Настройка логирования
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Создание клавиатуры с кнопками
keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Который час?")],
    [KeyboardButton(text="Курс доллара и евро в рублях?")],
    [KeyboardButton(text="Что за группа Анатоми?")],
    [KeyboardButton(text="Произвольный вопрос")]
], resize_keyboard=True)

@dp.message(Command(commands=['start']))
async def send_welcome(message: Message):
    await message.reply("Привет! Я эхо-бот. Отправь мне любое сообщение, и я отвечу тем же текстом.", reply_markup=keyboard)

@dp.message()
async def handle_message(message: Message):
    if message.text == "Который час?":
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        await message.reply(f"Текущее время: {current_time}")
    elif message.text == "Курс доллара и евро в рублях?":
        usd_rate, eur_rate = get_currency_rates()
        await message.reply(f"Курс доллара: {usd_rate} руб.\nКурс евро: {eur_rate} руб.")
    elif message.text == "Что за группа Анатоми?":
        inline_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Перейти в канал", url="https://t.me/anatomy_fire")]
        ])
        await message.reply("Вы узнаете все в нашем телеграм канале", reply_markup=inline_kb)
    elif message.text == "Произвольный вопрос":
        await message.reply("Это произвольный ответ на ваш вопрос.")
    else:
        await message.answer(message.text)

def get_currency_rates():
    url = 'https://www.cbr.ru/scripts/XML_daily.asp'
    response = urllib.request.urlopen(url)
    data = response.read()
    root = ET.fromstring(data)

    usd_rate = None
    eur_rate = None

    for valute in root.findall('Valute'):
        if valute.find('CharCode').text == 'USD':
            usd_rate = float(valute.find('Value').text.replace(',', '.'))
        elif valute.find('CharCode').text == 'EUR':
            eur_rate = float(valute.find('Value').text.replace(',', '.'))

    return usd_rate, eur_rate

async def main():
    # Удаление вебхука
    await bot.delete_webhook(drop_pending_updates=True)
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
