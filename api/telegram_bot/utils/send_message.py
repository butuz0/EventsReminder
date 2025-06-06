from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from django.conf import settings
import asyncio


async def send_message_async(chat_id: int, text) -> None:
    session = AiohttpSession()
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN,
              session=session,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    try:
        await bot.send_message(chat_id=chat_id, text=text)
    finally:
        await bot.session.close()


def send_message(chat_id: int, text: str) -> None:
    asyncio.run(send_message_async(chat_id, text))
