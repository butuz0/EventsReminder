from django.urls import reverse
from apps.notifications.tests.factories import NotificationFactory
from apps.events.tests.factories import EventFactory
from rest_framework.test import APIClient
import pytest


@pytest.fixture
def client(normal_user):
    client = APIClient()
    client.force_authenticate(user=normal_user)
    return client


@pytest.mark.django_db
def test_notification_by_event_list(client, normal_user):
    event = EventFactory(created_by=normal_user)
    NotificationFactory.create_batch(3, event=event, created_by=normal_user)
    NotificationFactory.create_batch(2)

    response = client.get(
        reverse('event-notifications', kwargs={'event_id': event.id})
    )

    assert response.status_code == 200
    assert len(response.data['results']) == 3


@pytest.mark.django_db
def test_notification_by_user_list(client, normal_user):
    NotificationFactory.create_batch(3, created_by=normal_user)
    NotificationFactory.create_batch(2)

    response = client.get(reverse('user-notification'))

    assert response.status_code == 200
    assert len(response.data['results']) == 3
    assert all(str(n['created_by']) == str(normal_user.id) for n in response.data['results'])
