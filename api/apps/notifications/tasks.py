from django.contrib.auth import get_user_model
from apps.events.models import Event
from .models import Notification
from .emails import send_notification_email
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
