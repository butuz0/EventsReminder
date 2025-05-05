from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties
from telegram_bot.handlers import register_handlers
from django.conf import settings


async def main():
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())

    register_handlers(dp)

    print('Deleting webhook...')
    await bot.delete_webhook(drop_pending_updates=True)
    
    print('Starting polling...')
    await dp.start_polling(bot)
