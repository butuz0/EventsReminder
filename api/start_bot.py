from telegram_bot.setup_django import setup_django
setup_django()
    
from telegram_bot.main import main
import asyncio


if __name__ == '__main__':
    asyncio.run(main())
