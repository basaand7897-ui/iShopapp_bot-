import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from config import BOT_TOKEN
from handlers import router
from db import init_db
from scheduler import setup_scheduler
from flask import Flask
import threading

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
web_app = Flask(__name__)

@web_app.route('/')
def index():
    return "Bot is running!"

@web_app.route('/health')
def health():
    return "OK"

async def main():
    init_db()
    dp.include_router(router)
    setup_scheduler(bot)
    await bot.set_my_commands([
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="features", description="Все функции бота")
    ])
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    threading.Thread(target=lambda: web_app.run(host="0.0.0.0", port=8080)).start()
    asyncio.run(main())
