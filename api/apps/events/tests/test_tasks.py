from django.utils import timezone
from .factories import EventFactory, RecurringEventFactory
from apps.events.tasks import update_next_event_occurrence_task
from apps.events.models import RecurringEvent
from datetime import timedelta
from unittest.mock import patch
from faker import Faker
import pytest

fake = Faker()


@pytest.mark.django_db
@patch('apps.events.tasks.update_next_event_occurrence_task.apply_async')
def test_update_next_occurrence_success(apply_async):
    event = EventFactory(start_datetime=timezone.now() - timedelta(days=1))
    recurring = RecurringEventFactory(
        event=event,
        recurrence_rule=RecurringEvent.RecurrenceRule.WEEKLY,
        recurrence_end_datetime=None
    )

    expected_next = recurring.calculate_next_occurrence()
    apply_async.return_value.id = fake.uuid4()

    update_next_event_occurrence_task(str(recurring.id))
    event.refresh_from_db()

    assert event.start_datetime == expected_next
    apply_async.assert_called_once_with(
        args=[str(recurring.id)],
        eta=expected_next
    )


@pytest.mark.django_db
@patch('apps.events.tasks.update_next_event_occurrence_task.apply_async')
def test_update_next_occurrence_no_next(apply_async):
    now = timezone.now()
    event = EventFactory(start_datetime=now - timedelta(days=1))
    recurring = RecurringEventFactory(
        event=event,
        recurrence_rule=RecurringEvent.RecurrenceRule.MONTHLY,
        recurrence_end_datetime=now
    )

    update_next_event_occurrence_task(str(recurring.id))

    apply_async.assert_not_called()


@pytest.mark.django_db
def test_update_next_occurrence_recurring_event_does_not_exist():
    result = update_next_event_occurrence_task(str(fake.uuid4()))
    assert result is None
