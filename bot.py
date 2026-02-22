import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

from openai import OpenAI

TELEGRAM_TOKEN = "7740778209:AAFULuUEq_GRgmIigT8PG2F_dlWjE2YgHew"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

client = OpenAI(api_key=OPENAI_API_KEY)

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Привет! Я бот с AI 🤖\nНапиши вопрос — я отвечу.")

@dp.message()
async def ai_reply(message: Message):
    if not OPENAI_API_KEY:
        await message.answer("Не найден OPENAI_API_KEY. Проверь setx и перезапуск cmd.")
        return

    text = (message.text or "").strip()
    if not text:
        await message.answer("Пока понимаю только текст 🙂")
        return

    try:
        resp = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {"role": "system", "content": "Ты полезный ассистент. Отвечай по-русски."},
                {"role": "user", "content": text},
            ],
        )
        await message.answer(resp.output_text.strip() or "Пустой ответ 🤔")
    except Exception as e:
        await message.answer(f"Ошибка OpenAI: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())