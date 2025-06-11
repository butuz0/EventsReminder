from django.utils.timezone import now, timedelta
from .factories import NotificationFactory
from apps.notifications.models import Notification
from apps.notifications.serializers import NotificationSerializer
from apps.users.tests.factories import UserFactory
from apps.profiles.tests.factories import ProfileWithTelegramFactory
from apps.events.tests.factories import EventFactory, RecurringEventFactory
from rest_framework.test import APIRequestFactory
from faker import Faker
import pytest

fake = Faker()


def get_request(user):
    factory = APIRequestFactory()
    request = factory.post('/fake-url')
    request.user = user
    return request


@pytest.mark.django_db
def test_notification_create_success(normal_user):
    event = EventFactory(
        created_by=normal_user,
        start_datetime=now() + timedelta(days=2)
    )

    data = {
        'event': event.id,
        'notification_datetime': (now() + timedelta(days=1)).isoformat()
    }

    serializer = NotificationSerializer(data=data, context={'request': get_request(normal_user)})
    assert serializer.is_valid()

    instance = serializer.save()
    assert instance.created_by == normal_user


@pytest.mark.django_db
def test_notification_retrieve(normal_user):
    notification = NotificationFactory()

    serializer = NotificationSerializer(instance=notification)
    data = serializer.data

    assert data['created_by'] == str(notification.created_by.id)


@pytest.mark.django_db
def test_notification_in_past(normal_user):
    event = EventFactory(
        created_by=normal_user,
        start_datetime=now() + timedelta(days=1)
    )

    data = {
        'event': event.id,
        'notification_datetime': (now() - timedelta(days=1)).isoformat()
    }
    serializer = NotificationSerializer(
        data=data,
        context={'request': get_request(normal_user)}
    )
    assert not serializer.is_valid()

    assert 'notification_datetime' in serializer.errors
    assert serializer.errors['notification_datetime'][0] == 'Notification datetime cannot be in the past.'


@pytest.mark.django_db
def test_notification_create_no_event(normal_user):
    data = {
        'notification_datetime': (now() + timedelta(days=1)).isoformat()
    }

    serializer = NotificationSerializer(
        data=data,
        context={'request': get_request(normal_user)}
    )
    assert not serializer.is_valid()

    assert 'notification_datetime' in serializer.errors
    assert serializer.errors['notification_datetime'][0] == 'Event is required.'


@pytest.mark.django_db
def test_notification_create_event_does_not_exist(normal_user):
    data = {
        'event': fake.uuid4(),
        'notification_datetime': (now() + timedelta(days=1)).isoformat()
    }

    serializer = NotificationSerializer(
        data=data,
        context={'request': get_request(normal_user)}
    )
    assert not serializer.is_valid()

    assert 'event' in serializer.errors
    assert serializer.errors['event'][0] == 'Event does not exist.'


@pytest.mark.django_db
def test_notification_after_recurring_end(normal_user):
    event = EventFactory(
        created_by=normal_user,
        start_datetime=now() + timedelta(days=3),
        is_recurring=True
    )
    RecurringEventFactory(
        event=event,
        recurrence_end_datetime=now() + timedelta(days=1)
    )

    data = {
        'event': event.id,
        'notification_datetime': (now() + timedelta(days=2)).isoformat()
    }
    serializer = NotificationSerializer(
        data=data,
        context={'request': get_request(normal_user)}
    )
    assert not serializer.is_valid()

    assert 'notification_datetime' in serializer.errors
    assert serializer.errors['notification_datetime'][0] == 'Notification must be before recurring event end time.'


@pytest.mark.django_db
def test_notification_after_event_start(normal_user):
    event = EventFactory(
        created_by=normal_user,
        start_datetime=now() + timedelta(days=1)
    )

    data = {
        'event': event.id,
        'notification_datetime': (now() + timedelta(days=2)).isoformat()
    }
    serializer = NotificationSerializer(
        data=data,
        context={'request': get_request(normal_user)}
    )
    assert not serializer.is_valid()

    assert 'notification_datetime' in serializer.errors
    assert serializer.errors['notification_datetime'][0] == 'Notification must be before event start time.'


@pytest.mark.django_db
def test_notification_create_no_permission(normal_user):
    other = UserFactory()
    event = EventFactory(
        created_by=other,
        start_datetime=now() + timedelta(days=1)
    )

    data = {
        'event': event.id,
        'notification_datetime': (now() + timedelta(hours=1)).isoformat()
    }

    serializer = NotificationSerializer(data=data, context={'request': get_request(normal_user)})

    assert not serializer.is_valid()
    assert 'non_field_errors' in serializer.errors
    assert (serializer.errors['non_field_errors'][
                0] == 'You do not have permission to create notifications for this event.')


@pytest.mark.django_db
def test_notification_create_telegram_success():
    user = ProfileWithTelegramFactory(
        telegram__is_verified=True
    ).user
    event = EventFactory(
        created_by=user,
        start_datetime=now() + timedelta(days=1)
    )

    data = {
        'event': event.id,
        'notification_method': Notification.NotificationMethod.TELEGRAM,
        'notification_datetime': (now() + timedelta(hours=1)).isoformat()
    }
    serializer = NotificationSerializer(
        data=data,
        context={'request': get_request(user)}
    )
    assert serializer.is_valid()


@pytest.mark.django_db
def test_notification_create_telegram_not_verified():
    user = ProfileWithTelegramFactory(
        telegram__is_verified=False
    ).user
    event = EventFactory(
        created_by=user,
        start_datetime=now() + timedelta(days=1)
    )

    data = {
        'event': event.id,
        'notification_method': Notification.NotificationMethod.TELEGRAM,
        'notification_datetime': (now() + timedelta(hours=1)).isoformat()
    }
    serializer = NotificationSerializer(
        data=data,
        context={'request': get_request(user)}
    )
    assert not serializer.is_valid()

    assert 'non_field_errors' in serializer.errors
    assert serializer.errors['non_field_errors'][0] == 'Your Telegram account is not connected yet.'
