from django.core.management.base import BaseCommand
from django.utils.timezone import now
from apps.notifications.models import Notification
from apps.notifications.tasks import send_notification_email_task, send_notification_telegram_message_task
from celery.result import AsyncResult


class Command(BaseCommand):
    help = 'Schedule all future, unsent notifications in Celery'

    def handle(self, *args, **kwargs):
        notifications = Notification.objects.filter(
            is_sent=False,
            notification_datetime__gt=now()
        )

        if not notifications.exists():
            self.stdout.write(self.style.SUCCESS('No unsent notifications found.'))
            return

        scheduled = 0
        for n in notifications:
            result = AsyncResult(n.celery_task_id)
            if result.status in ['PENDING', 'RECEIVED', 'STARTED', 'RETRY']:
                self.stdout.write(f"Notification {n.id} already scheduled as task {n.celery_task_id}")
                continue

            task = None
            if n.notification_method == Notification.NotificationMethod.EMAIL:
                task = send_notification_email_task.apply_async(
                    args=[n.event.id, n.created_by.id, n.id],
                    eta=n.notification_datetime)

            elif n.notification_method == Notification.NotificationMethod.TELEGRAM:
                task = send_notification_telegram_message_task.apply_async(
                    args=[n.event.id, n.created_by.id, n.id],
                    eta=n.notification_datetime)

            n.celery_task_id = task.id
            n.save(update_fields=['celery_task_id'])
            scheduled += 1

        self.stdout.write(self.style.SUCCESS(
            f'{scheduled} notification(s) scheduled.'
        ))
