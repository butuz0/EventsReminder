from django.utils import timezone
from .factories import NotificationFactory
from apps.notifications.models import Notification
from apps.profiles.tests.factories import UserWithProfileFactory
from apps.events.tests.factories import EventFactory
from unittest.mock import patch, MagicMock
from datetime import timedelta
import pytest


@pytest.mark.django_db
@patch('apps.notifications.signals.send_notification_email_task.apply_async')
def test_create_celery_notification_task_email(apply_async, normal_user):
    apply_async.return_value.id = 'celery-task-id-1'

    event = EventFactory(created_by=normal_user)

    notification = Notification.objects.create(
        event=event,
        created_by=normal_user,
        notification_method=Notification.NotificationMethod.EMAIL,
        notification_datetime=timezone.now() + timedelta(hours=1)
    )

    apply_async.assert_called_once_with(
        args=[notification.event.id, notification.created_by.id, notification.id],
        eta=notification.notification_datetime
    )

    notification.refresh_from_db()
    assert notification.celery_task_id == 'celery-task-id-1'


@pytest.mark.django_db
@patch('apps.notifications.signals.send_notification_telegram_message_task.apply_async')
def test_create_celery_notification_task_telegram(apply_async):
    apply_async.return_value.id = 'celery-task-id-2'

    user = UserWithProfileFactory(profile__telegram__is_verified=True)
    event = EventFactory(created_by=user)

    notification = Notification.objects.create(
        event=event,
        created_by=user,
        notification_method=Notification.NotificationMethod.TELEGRAM,
        notification_datetime=timezone.now() + timedelta(hours=1)
    )

    apply_async.assert_called_once_with(
        args=[event.id, user.id, notification.id],
        eta=notification.notification_datetime
    )

    notification.refresh_from_db()
    assert notification.celery_task_id == 'celery-task-id-2'


@pytest.mark.django_db
@patch('apps.notifications.signals.current_app.control.revoke')
def test_delete_celery_notification_task(revoke):
    user = UserWithProfileFactory(profile__telegram__is_verified=True)
    event = EventFactory(created_by=user)

    notification = Notification.objects.create(
        event=event,
        created_by=user,
        notification_method=Notification.NotificationMethod.EMAIL,
        notification_datetime=timezone.now() + timedelta(hours=1)
    )

    notification.refresh_from_db()
    celery_task_id = notification.celery_task_id

    notification.delete()

    revoke.assert_called_once_with(celery_task_id, terminate=True)
