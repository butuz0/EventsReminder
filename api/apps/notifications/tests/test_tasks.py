from .factories import NotificationFactory
from apps.notifications.tasks import (
    send_notification_email_task,
    send_notification_telegram_message_task
)
from apps.profiles.tests.factories import ProfileWithTelegramFactory
from apps.events.tests.factories import EventFactory
from unittest.mock import patch
import pytest


@pytest.mark.django_db
@patch('apps.notifications.tasks.send_notification_email')
def test_send_notification_email_task_success(send_email):
    notification = NotificationFactory()
    event = notification.event
    user = notification.created_by

    send_notification_email_task(str(event.id), str(user.id), str(notification.id))

    send_email.assert_called_once_with(user, event)

    notification.refresh_from_db()
    assert notification.is_sent is True


@pytest.mark.django_db
@patch('apps.notifications.tasks.send_message')
@patch('apps.notifications.tasks.generate_event_reminder_text')
def test_send_notification_telegram_task_success(generate_text, send_message):
    user = ProfileWithTelegramFactory().user
    event = EventFactory(created_by=user)
    notification = NotificationFactory(event=event, created_by=user)

    generate_text.return_value = 'Reminder text'

    send_notification_telegram_message_task(str(event.id), str(user.id), str(notification.id))

    generate_text.assert_called_once_with(event)

    telegram_id = user.profile.telegram.telegram_user_id
    send_message.assert_called_once_with(telegram_id, 'Reminder text')

    notification.refresh_from_db()
    assert notification.is_sent is True
