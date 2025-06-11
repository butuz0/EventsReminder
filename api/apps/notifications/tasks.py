from django.contrib.auth import get_user_model
from apps.events.models import Event
from .models import Notification
from .emails import send_notification_email
from telegram_bot.utils.generate_reminder import generate_event_reminder_text
from telegram_bot.utils.send_message import send_message
from celery import shared_task

User = get_user_model()


@shared_task
def send_notification_email_task(event_id, user_id, notification_id):
    event = Event.objects.get(id=event_id)
    user = User.objects.get(id=user_id)

    send_notification_email(user, event)

    notification = Notification.objects.get(id=notification_id)
    notification.is_sent = True
    notification.save(update_fields=['is_sent'])


@shared_task
def send_notification_telegram_message_task(event_id, user_id, notification_id):
    event = Event.objects.get(id=event_id)
    user = User.objects.get(id=user_id)

    text = generate_event_reminder_text(event)
    user_id = user.profile.telegram.telegram_user_id

    send_message(user_id, text)

    notification = Notification.objects.get(id=notification_id)
    notification.is_sent = True
    notification.save(update_fields=['is_sent'])
