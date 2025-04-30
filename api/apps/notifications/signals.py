from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import now, timedelta
from .models import Notification
from .tasks import send_notification_email_task
from celery import current_app


@receiver(post_save, sender=Notification)
def create_celery_notification_task(sender, instance: Notification, created: bool, **kwargs):
    if created:
        eta = instance.notification_datetime
        task = send_notification_email_task.apply_async(
            args=[instance.event.id, instance.created_by.id, instance.id], 
            eta=eta)
        instance.celery_task_id = task.id
        instance.save(update_fields=['celery_task_id'])


@receiver(post_delete, sender=Notification)
def delete_celery_notification_task(sender, instance: Notification, **kwargs):
    if instance.celery_task_id:
        current_app.control.revoke(instance.celery_task_id, terminate=True)
