from .models import TelegramData
from telegram_bot.utils.send_message import send_message
from telegram_bot.utils.update_auth_state import set_user_verified_state
from telegram_bot.messages.verification import MESSAGES
from celery import shared_task


@shared_task(bind=True, max_retries=10, default_retry_delay=2)
def send_telegram_greeting(self, chat_id: int):
    try:
        send_message(chat_id, MESSAGES['verification_successful'])
        set_user_verified_state(chat_id)
        TelegramData.objects.filter(telegram_user_id=chat_id).update(is_verified=True)
    except Exception as e:
        raise self.retry(exc=e)
