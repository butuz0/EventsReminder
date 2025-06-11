from apps.profiles.tasks import send_telegram_greeting
from apps.profiles.tests.factories import TelegramDataFactory
from telegram_bot.messages.verification import MESSAGES
from unittest.mock import patch
import pytest


@pytest.mark.django_db
@patch('apps.profiles.tasks.send_message')
@patch('apps.profiles.tasks.set_user_verified_state')
def test_send_telegram_greeting(mock_set_user_verified_state, mock_send_message):
    telegram_data = TelegramDataFactory(is_verified=False)
    chat_id = telegram_data.telegram_user_id

    send_telegram_greeting(chat_id)
    mock_send_message.assert_called_once_with(chat_id, MESSAGES['verification_successful'])
    mock_set_user_verified_state.assert_called_once_with(chat_id)

    telegram_data.refresh_from_db()

    assert telegram_data.is_verified is True
