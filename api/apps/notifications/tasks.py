from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from apps.events.models import Event
from apps.registration_cards.models import RegistrationCard
from .models import Notification
from .emails import send_event_notification_email
from telegram_bot.utils.generate_reminder import generate_event_reminder_text
from telegram_bot.utils.send_message import send_message
from celery import shared_task

User = get_user_model()


@shared_task
def send_notification_email_task(content_type_id, object_id, user_id, notification_id):
    user = User.objects.get(id=user_id)
    content_type = ContentType.objects.get(id=content_type_id)
    model_class = content_type.model_class()

    obj = model_class.objects.get(id=object_id)

    if isinstance(obj, Event):
        send_event_notification_email(user, obj)
    elif isinstance(obj, RegistrationCard):
        pass

    notification = Notification.objects.get(id=notification_id)
    notification.is_sent = True
    notification.save(update_fields=['is_sent'])


@shared_task
def send_notification_telegram_message_task(content_type_id, object_id, user_id, notification_id):
    user = User.objects.get(id=user_id)
    content_type = ContentType.objects.get(id=content_type_id)
    model_class = content_type.model_class()

    obj = model_class.objects.get(id=object_id)
    user_id = user.profile.telegram.telegram_user_id

    if isinstance(obj, Event):
        text = generate_event_reminder_text(obj)
        send_message(user_id, text)
    elif isinstance(obj, RegistrationCard):
        pass

    notification = Notification.objects.get(id=notification_id)
    notification.is_sent = True
    notification.save(update_fields=['is_sent'])
