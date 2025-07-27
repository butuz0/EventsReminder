from django.core.management.base import BaseCommand
from apps.notifications.models import Notification
from apps.notifications.tasks import send_notification_email_task, send_notification_telegram_message_task
from apps.common.celery import reschedule_celery_task


class Command(BaseCommand):
    help = 'Schedule all unsent notifications in Celery'

    def handle(self, *args, **kwargs):
        notifications = Notification.objects.filter(is_sent=False)

        if not notifications.exists():
            self.stdout.write(self.style.SUCCESS('No unsent notifications found.'))
            return

        scheduled = 0
        for n in notifications:
            task = None

            if n.notification_method == Notification.NotificationMethod.EMAIL:
                task = send_notification_email_task
            elif n.notification_method == Notification.NotificationMethod.TELEGRAM:
                task = send_notification_telegram_message_task

            if task is None:
                self.stdout.write(self.style.WARNING(
                    f'Notification {n.id} skipped: '
                    f'unknown notification method "{n.notification_method}"'
                ))
                continue

            reschedule_celery_task(
                instance=n,
                celery_task=task,
                task_args=[n.content_type.id, n.object_id, n.created_by.id, n.id],
                eta=n.notification_datetime,
                task_id_field='celery_task_id',
                save=True
            )
            scheduled += 1

        self.stdout.write(self.style.SUCCESS(
            f'{scheduled} notification(s) scheduled.'
        ))
