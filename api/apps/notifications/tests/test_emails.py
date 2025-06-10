from .factories import EventFactory
from apps.profiles.tests.factories import UserWithProfileFactory
from apps.notifications.emails import send_notification_email
from config.settings.local import SITE_NAME, DEFAULT_FROM_EMAIL
from unittest.mock import patch
import pytest


@pytest.mark.django_db
@patch('apps.notifications.emails.EmailMultiAlternatives')
@patch('apps.notifications.emails.render_to_string')
def test_send_notification_email(render_to_string, email_class):
    user = UserWithProfileFactory()
    event = EventFactory()

    render_to_string.side_effect = ['HTML email', 'Text email']
    mock_email_instance = email_class.return_value

    send_notification_email(user, event)

    assert render_to_string.call_count == 2
    render_to_string.assert_any_call('notifications/notification_email.html', {
        'user': user,
        'event': event,
        'site_name': SITE_NAME
    })
    render_to_string.assert_any_call('notifications/notification_email.txt', {
        'user': user,
        'event': event,
        'site_name': SITE_NAME
    })

    email_class.assert_called_once_with(
        f'Notification for {event}',
        'Text email',
        DEFAULT_FROM_EMAIL,
        [user.email],
    )

    mock_email_instance.attach_alternative.assert_called_once_with('HTML email', 'text/html')
    mock_email_instance.send.assert_called_once()
