from django.conf import settings
from aiogram import Bot
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.context import FSMContext
from api.telegram_bot.handlers.states import VerificationStates
import asyncio


async def set_user_state_async(bot_token: str, redis_url: str, chat_id: int, state_cls):
    bot = Bot(token=bot_token)
    storage = RedisStorage.from_url(redis_url)
    context = FSMContext(storage=storage, key=StorageKey(bot.id, chat_id, chat_id))
    await context.set_state(state_cls)
    await bot.session.close()


def set_user_verified_state(chat_id: int):
    asyncio.run(
        set_user_state_async(
            bot_token=settings.TELEGRAM_BOT_TOKEN,
            redis_url=settings.REDIS_URL,
            chat_id=chat_id,
            state_cls=VerificationStates.verified
        )
    )
