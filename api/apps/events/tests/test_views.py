from django.urls import reverse
from django.utils import timezone
from .factories import EventFactory, RecurringEventFactory
from apps.events.models import Event, RecurringEvent
from apps.users.tests.factories import UserFactory
from rest_framework.test import APIClient
from datetime import timedelta
from faker import Faker
import pytest

fake = Faker()


@pytest.fixture
def client(normal_user):
    client = APIClient()
    client.force_authenticate(user=normal_user)
    return client


@pytest.mark.django_db
def test_my_events_list(client, normal_user):
    EventFactory.create_batch(3, created_by=normal_user)
    EventFactory.create_batch(2, assigned_to=[normal_user])
    EventFactory.create_batch(2)

    response = client.get(reverse('my-events-list'))

    assert response.status_code == 200
    assert len(response.data['results']) == 5


@pytest.mark.django_db
def test_event_update_success(client, normal_user):
    event = EventFactory(
        created_by=normal_user,
        title='Old title'
    )
    data = {'title': 'New title'}

    response = client.patch(
        reverse('event-update', kwargs={'id': event.id}),
        data=data,
        format='json'
    )

    assert response.status_code == 200
    assert response.data['id'] == str(event.id)
    assert response.data['title'] == 'New title'


@pytest.mark.django_db
def test_event_update_not_created_by_user(client, normal_user):
    event = EventFactory(title='Old title')

    response = client.patch(
        reverse('event-update', kwargs={'id': event.id})
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_event_delete_success(client, normal_user):
    event = EventFactory(created_by=normal_user)

    response = client.delete(
        reverse('event-delete', kwargs={'id': event.id})
    )

    assert response.status_code == 204
    assert not Event.objects.filter(id=event.id).exists()


@pytest.mark.django_db
def test_event_delete_not_created_by_user(client, normal_user):
    event = EventFactory()

    response = client.delete(
        reverse('event-delete', kwargs={'id': event.id})
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_event_leave_success(client, normal_user):
    event = EventFactory(assigned_to=[normal_user])

    response = client.delete(
        reverse('event-leave', kwargs={'id': event.id})
    )

    assert response.status_code == 204
    event.refresh_from_db()

    assert not event.assigned_to.exists()


@pytest.mark.django_db
def test_event_leave_user_not_assigned(client, normal_user):
    other_user = UserFactory()
    event = EventFactory(assigned_to=[other_user])

    response = client.delete(
        reverse('event-leave', kwargs={'id': event.id})
    )

    assert response.status_code == 403
    assert response.data['detail'] == 'You cannot leave the event because you have never been assigned to it.Ви не можете відмовитись від події, оскільки вона Вам не призначена.'


@pytest.mark.django_db
def test_event_leave_event_does_not_exist(client, normal_user):
    event_id = fake.uuid4()

    response = client.delete(
        reverse('event-leave', kwargs={'id': event_id})
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_recurring_event_create_success(client, normal_user):
    event = EventFactory(created_by=normal_user, is_recurring=False)

    now = timezone.now()
    data = {
        'recurrence_rule': 'w',
        'recurrence_end_datetime': (now + timedelta(days=30)).isoformat(),
    }

    response = client.post(
        reverse('recurring-create', kwargs={'event_id': event.id}),
        data=data,
        format='json'
    )

    assert response.status_code == 201
    event.refresh_from_db()
    assert event.is_recurring is True
    assert RecurringEvent.objects.filter(event=event).exists()


@pytest.mark.django_db
def test_recurring_event_create_not_created_by_user(client, normal_user):
    other_user = UserFactory()
    event = EventFactory(created_by=other_user)

    now = timezone.now()
    data = {
        'recurrence_rule': RecurringEvent.RecurrenceRule.WEEKLY,
        'recurrence_end_datetime': (now + timedelta(days=30)).isoformat(),
    }

    response = client.post(
        reverse('recurring-create', kwargs={'event_id': event.id}),
        data=data,
        format='json'
    )

    assert response.status_code == 403
    assert response.data['detail'] == 'Тільки творець події може створити повторювану подію.'
    assert not RecurringEvent.objects.filter(event=event).exists()


@pytest.mark.django_db
def test_recurring_event_create_event_does_not_exist(client):
    event_id = fake.uuid4()

    response = client.post(
        reverse('recurring-create', kwargs={'event_id': event_id})
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_recurring_event_update_success(client, normal_user):
    event = EventFactory(created_by=normal_user)
    recurring = RecurringEventFactory(event=event)
    new_end = timezone.now() + timedelta(days=5)

    data = {
        'recurrence_end_datetime': new_end.isoformat(),
    }

    response = client.patch(
        reverse('recurring-update', kwargs={'event_id': event.id}),
        data=data,
        format='json'
    )

    assert response.status_code == 200
    recurring.refresh_from_db()
    assert recurring.recurrence_end_datetime == new_end


@pytest.mark.django_db
def test_recurring_event_update_not_created_by_user(client, normal_user):
    other_user = UserFactory()
    event = EventFactory(created_by=other_user)
    RecurringEventFactory(event=event)

    response = client.patch(
        reverse('recurring-update', kwargs={'event_id': event.id})
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_recurring_event_update_event_does_not_exist(client, normal_user):
    event_id = fake.uuid4()

    response = client.patch(
        reverse('recurring-update', kwargs={'event_id': event_id})
    )

    assert response.status_code == 404
