from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.client.bot import DefaultBotProperties
from telegram_bot.handlers import register_handlers
from django.conf import settings


async def main():
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    storage = RedisStorage.from_url(settings.REDIS_URL)

    dp = Dispatcher(storage=storage)

    register_handlers(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
