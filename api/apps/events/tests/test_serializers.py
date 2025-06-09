from django.utils import timezone
from .factories import EventFactory, RecurringEventFactory
from apps.events.models import Event, RecurringEvent
from apps.users.tests.factories import UserFactory
from apps.teams.tests.factories import TeamFactory
from apps.events.serializers import (
    RecurringEventSerializer,
    EventCreateSerializer,
    EventUpdateSerializer,
    EventDetailSerializer
)
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIRequestFactory
from unittest.mock import patch, Mock
from datetime import timedelta
from faker import Faker
import pytest

fake = Faker()


def get_context(event):
    return {'event': event}


def get_request(user):
    factory = APIRequestFactory()
    request = factory.post('/fake-url')
    request.user = user
    return request


@pytest.mark.django_db
def test_recurring_event_serializer_valid():
    now = timezone.now()
    event = EventFactory(start_datetime=now + timedelta(days=1))
    data = {
        'recurrence_rule': RecurringEvent.RecurrenceRule.WEEKLY,
        'recurrence_end_datetime': (now + timedelta(weeks=4))
    }

    serializer = RecurringEventSerializer(data=data, context=get_context(event))
    assert serializer.is_valid()
    instance = serializer.save()

    assert instance.event == event
    assert instance.recurrence_rule == data['recurrence_rule']


@pytest.mark.django_db
def test_recurring_event_serializer_end_in_past():
    now = timezone.now()
    event = EventFactory(start_datetime=now + timedelta(days=1))
    data = {
        'recurrence_rule': RecurringEvent.RecurrenceRule.DAILY,
        'recurrence_end_datetime': now - timedelta(days=1),
    }

    serializer = RecurringEventSerializer(data=data, context=get_context(event))
    with pytest.raises(ValidationError) as e:
        serializer.is_valid(raise_exception=True)

    errors = e.value.detail
    assert 'recurrence_end_datetime' in errors
    assert str(errors['recurrence_end_datetime'][0]) == 'End date must be in the future.'


@pytest.mark.django_db
def test_recurring_event_serializer_end_before_event_start():
    now = timezone.now()
    event_start = now + timedelta(days=3)
    recurrence_end = now + timedelta(days=1)

    event = EventFactory(start_datetime=event_start)
    data = {
        'recurrence_rule': RecurringEvent.RecurrenceRule.MONTHLY,
        'recurrence_end_datetime': recurrence_end,
    }

    serializer = RecurringEventSerializer(data=data, context=get_context(event))
    with pytest.raises(ValidationError) as e:
        serializer.is_valid(raise_exception=True)

    assert 'non_field_errors' in e.value.detail
    assert 'End date must be after event start date.' in str(e.value.detail['non_field_errors'][0])


@pytest.mark.django_db
def test_recurring_event_serializer_without_event():
    now = timezone.now()
    data = {
        'recurrence_rule': RecurringEvent.RecurrenceRule.DAILY,
        'recurrence_end_datetime': now + timedelta(days=1),
    }

    serializer = RecurringEventSerializer(data=data, context={})
    assert serializer.is_valid()

    with pytest.raises(ValidationError) as e:
        serializer.save()

    assert str(e.value.detail[0]) == 'Event must be provided.'


@pytest.mark.django_db
def test_recurring_event_serializer_update_valid():
    instance = RecurringEventFactory()
    now = timezone.now()
    new_end = now + timedelta(days=10)

    serializer = RecurringEventSerializer(
        instance,
        data={
            'recurrence_rule': instance.recurrence_rule,
            'recurrence_end_datetime': new_end
        },
        partial=True
    )

    assert serializer.is_valid()
    updated = serializer.save()

    assert updated.recurrence_end_datetime == new_end


@pytest.mark.django_db
def test_recurring_event_serializer_without_end_datetime():
    now = timezone.now()
    event = EventFactory(start_datetime=now + timedelta(days=1))
    data = {
        'recurrence_rule': RecurringEvent.RecurrenceRule.DAILY,
        'recurrence_end_datetime': None,
    }
    serializer = RecurringEventSerializer(data=data, context=get_context(event))
    assert serializer.is_valid()
    instance = serializer.save()

    assert instance.recurrence_end_datetime is None


@pytest.mark.django_db
def test_event_create_serializer_success(normal_user):
    data = {
        'title': 'Test title',
        'description': 'Test description',
        'start_datetime': (timezone.now() + timedelta(days=1)).isoformat(),
        'location': 'Test location',
        'link': 'https://example.com',
        'priority': Event.Priority.HIGH,
        'tags': ['test', 'tag'],
        'is_recurring': False,
    }

    context = {'request': get_request(normal_user)}
    serializer = EventCreateSerializer(data=data, context=context)

    assert serializer.is_valid()
    event = serializer.save()

    assert event.created_by == normal_user
    assert list(event.tags.names()) == ['test', 'tag']


@pytest.mark.django_db
def test_event_create_serializer_team_success(normal_user):
    members = UserFactory.create_batch(3)
    team = TeamFactory(created_by=normal_user, members=members)

    data = {
        'title': 'Test title',
        'description': 'Test description',
        'start_datetime': (timezone.now() + timedelta(days=1)).isoformat(),
        'location': 'Test location',
        'link': 'https://example.com',
        'priority': Event.Priority.HIGH,
        'tags': ['test', 'tag'],
        'assigned_to_ids': [member.id for member in members],
        'team': team.id,
        'is_recurring': False,
    }

    context = {'request': get_request(normal_user)}
    serializer = EventCreateSerializer(data=data, context=context)

    assert serializer.is_valid()
    event = serializer.save()

    assert event.created_by == normal_user
    assert event.team == team
    assert set(event.assigned_to.values_list('id', flat=True)) == set(member.id for member in members)
    assert list(event.tags.names()) == ['test', 'tag']


@pytest.mark.django_db
def test_event_create_serializer_invalid_datetime(normal_user):
    data = {
        'title': 'Test title',
        'description': 'Test description',
        'priority': Event.Priority.HIGH,
        'start_datetime': (timezone.now() - timedelta(days=1)).isoformat(),
        'location': 'Test location',
        'link': 'https://example.com',
        'tags': ['test', 'tag'],
        'is_recurring': False,
    }

    context = {'request': get_request(normal_user)}
    serializer = EventCreateSerializer(data=data, context=context)

    assert not serializer.is_valid()
    assert 'start_datetime' in serializer.errors
    assert serializer.errors['start_datetime'][0] == 'Event start time cannot be in the past.'


@pytest.mark.django_db
def test_event_create_serializer_assign_to_yourself(normal_user):
    team = TeamFactory(created_by=normal_user)

    data = {
        'title': 'Test title',
        'start_datetime': (timezone.now() + timedelta(days=1)).isoformat(),
        'priority': Event.Priority.HIGH,
        'assigned_to_ids': [normal_user.id],
        'team': team.id,
    }

    context = {'request': get_request(normal_user)}
    serializer = EventCreateSerializer(data=data, context=context)

    assert not serializer.is_valid()
    assert 'assigned_to_ids' in serializer.errors
    assert serializer.errors['assigned_to_ids'][0] == 'You cannot assign the event to yourself.'


@pytest.mark.django_db
def test_event_create_serializer_assigned_to_duplicates(normal_user):
    members = UserFactory.create_batch(3)
    team = TeamFactory(created_by=normal_user, members=members)

    data = {
        'title': 'Test title',
        'start_datetime': (timezone.now() + timedelta(days=1)).isoformat(),
        'priority': Event.Priority.HIGH,
        'assigned_to_ids': [member.id for member in members] + [members[0].id],
        'team': team.id,
    }

    context = {'request': get_request(normal_user)}
    serializer = EventCreateSerializer(data=data, context=context)

    assert not serializer.is_valid()
    assert 'assigned_to_ids' in serializer.errors
    assert serializer.errors['assigned_to_ids'][0] == 'Duplicate user IDs are not allowed.'


@pytest.mark.django_db
def test_event_create_serializer_assigned_to_does_not_exist(normal_user):
    member = UserFactory()
    fake_user_id = fake.uuid4()
    team = TeamFactory(created_by=normal_user, members=[member])

    data = {
        'title': 'Test title',
        'start_datetime': (timezone.now() + timedelta(days=1)).isoformat(),
        'priority': Event.Priority.HIGH,
        'assigned_to_ids': [member.id, fake_user_id],
        'team': team.id,
    }

    context = {'request': get_request(normal_user)}
    serializer = EventCreateSerializer(data=data, context=context)

    with pytest.raises(ValidationError) as e:
        serializer.is_valid(raise_exception=True)

    assert 'assigned_to_ids' in serializer.errors
    assert 'Users with the following IDs do not exist' in str(e.value.detail['assigned_to_ids'][0])


@pytest.mark.django_db
def test_event_create_serializer_team_does_not_exist(normal_user):
    team_id = fake.uuid4()

    data = {
        'title': 'Test title',
        'start_datetime': (timezone.now() + timedelta(days=1)).isoformat(),
        'priority': Event.Priority.HIGH,
        'team': team_id,
    }

    context = {'request': get_request(normal_user)}
    serializer = EventCreateSerializer(data=data, context=context)

    assert not serializer.is_valid()
    assert 'team' in serializer.errors
    assert serializer.errors['team'][0] == 'Team does not exist.'


@pytest.mark.django_db
def test_event_create_serializer_not_team_creator(normal_user):
    other_user = UserFactory()
    team = TeamFactory(created_by=other_user)

    data = {
        'title': 'Test title',
        'start_datetime': (timezone.now() + timedelta(days=1)).isoformat(),
        'priority': Event.Priority.HIGH,
        'team': team.id,
    }

    context = {'request': get_request(normal_user)}
    serializer = EventCreateSerializer(data=data, context=context)

    assert not serializer.is_valid()
    assert 'team' in serializer.errors
    assert serializer.errors['team'][0] == 'Only team owner can create events.'


@pytest.mark.django_db
def test_event_create_serializer_not_team_members(normal_user):
    member = UserFactory()
    not_member = UserFactory()
    team = TeamFactory(created_by=normal_user, members=[member])

    data = {
        'title': 'Test title',
        'start_datetime': (timezone.now() + timedelta(days=1)).isoformat(),
        'priority': Event.Priority.HIGH,
        'team': team.id,
        'assigned_to_ids': [member.id, not_member.id],
    }

    context = {'request': get_request(normal_user)}
    serializer = EventCreateSerializer(data=data, context=context)

    assert not serializer.is_valid()
    assert 'The following users are not members of the selected team' in serializer.errors['non_field_errors'][0]


@pytest.mark.django_db
@patch('apps.events.serializers.reschedule_recurring_event')
def test_event_update_serializer_full_update(reschedule_recurring_event, normal_user):
    assigned_to_old = UserFactory.create_batch(2)
    assigned_to_new = UserFactory.create_batch(2)
    tags_old = ['old', 'tags']
    tags_new = ['updated', 'important']

    team = TeamFactory(
        created_by=normal_user,
        members=assigned_to_old + assigned_to_new
    )

    event = EventFactory(
        created_by=normal_user,
        priority=Event.Priority.LOW,
        team=team,
        assigned_to=assigned_to_old,
        is_recurring=True,
        tags=tags_old,
        start_datetime=timezone.now() + timedelta(days=1)
    )

    recurring_event = RecurringEventFactory(event=event)

    new_datetime = event.start_datetime + timedelta(days=5)

    data = {
        'title': 'Updated title',
        'description': 'Updated description',
        'start_datetime': new_datetime.isoformat(),
        'location': "New Location",
        'link': 'https://new.example.com',
        'priority': Event.Priority.CRITICAL,
        'tags': tags_new,
        'assigned_to_ids': [user.id for user in assigned_to_new],
    }

    context = {'request': get_request(normal_user)}
    serializer = EventUpdateSerializer(
        instance=event,
        data=data,
        context=context,
        partial=True
    )
    assert serializer.is_valid()

    updated = serializer.save()
    assert updated.title == data['title']
    assert updated.description == data['description']
    assert updated.start_datetime == new_datetime
    assert updated.location == data['location']
    assert updated.link == data['link']
    assert updated.priority == data['priority']
    assert list(updated.tags.names()) == tags_new
    assert set(updated.assigned_to.values_list('id', flat=True)) == set(u.id for u in assigned_to_new)
    reschedule_recurring_event.assert_called_once_with(recurring_event)


@pytest.mark.django_db
def test_event_update_serializer_cancel_recurring_event(normal_user):
    event = EventFactory(
        created_by=normal_user,
        start_datetime=timezone.now() + timedelta(days=1),
        is_recurring=True
    )
    RecurringEventFactory(event=event)

    context = {'request': get_request(normal_user)}
    serializer = EventUpdateSerializer(
        instance=event,
        data={'is_recurring': False},
        context=context,
        partial=True
    )
    assert serializer.is_valid()

    updated = serializer.save()
    assert updated.is_recurring is False
    assert not RecurringEvent.objects.filter(event=event).exists()


@pytest.mark.django_db
def test_event_detail_serializer_full_data(normal_user):
    assigned_to = UserFactory.create_batch(2)
    team = TeamFactory(created_by=normal_user, members=assigned_to)

    event = EventFactory(
        created_by=normal_user,
        team=team,
        assigned_to=assigned_to,
        is_recurring=True,
        start_datetime=timezone.now() + timedelta(days=1),
        tags=['important', 'tags'],
        image=None
    )

    recurring_event = RecurringEventFactory(event=event)

    context = {'request': get_request(normal_user)}
    serializer = EventDetailSerializer(event, context=context)
    data = serializer.data

    assert data['title'] == event.title
    assert data['description'] == event.description
    assert data['priority'] == event.priority
    assert data['is_recurring'] is True
    assert data['created_by']['id'] == str(normal_user.id)
    assert len(data['assigned_to']) == 2
    assert data['tags'] == ['important', 'tags']
    assert data['image_url'] is None

    assert data['team'] == {
        'id': str(team.id),
        'name': team.name
    }

    assert data['recurring_event'] is not None
    assert data['recurring_event']['recurrence_rule'] == recurring_event.recurrence_rule


@pytest.mark.django_db
def test_event_detail_serializer_no_team_no_image_no_recurring(normal_user):
    event = EventFactory(team=None, image=None, is_recurring=False)

    context = {'request': get_request(normal_user)}
    serializer = EventDetailSerializer(event, context=context)
    data = serializer.data

    assert data['team'] is None
    assert data['image_url'] is None
    assert data['recurring_event'] is None


@pytest.mark.django_db
def test_event_detail_serializer_image_url():
    event = EventFactory()

    factory = APIRequestFactory()
    request = factory.get('/fake-request')
    serializer = EventDetailSerializer(event, context={'request': request})

    assert serializer.data['image_url'] == request.build_absolute_uri(event.image.url)


@pytest.mark.django_db
def test_event_detail_serializer_image_url_local():
    event = EventFactory()
    mocked_request = Mock()
    mocked_request.build_absolute_uri.return_value = 'http://localhost/media/image.jpg'

    serializer = EventDetailSerializer(event, context={'request': mocked_request})

    assert serializer.data['image_url'] == 'http://localhost:8080/media/image.jpg'
