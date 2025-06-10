from .factories import NotificationFactory
import pytest


@pytest.mark.django_db
def test_notification_str():
    notification = NotificationFactory()
    assert str(notification) == f'{notification.event.title} - {notification.get_notification_method_display()}'
