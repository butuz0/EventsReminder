from telegram_bot.setup_django import setup_django
from telegram_bot.main import main
import asyncio

setup_django()

if __name__ == '__main__':
    asyncio.run(main())
