from django.utils import timezone
from .factories import EventFactory, RecurringEventFactory
from apps.events.models import RecurringEvent
from datetime import timedelta
import pytest


@pytest.mark.django_db
def test_event_str():
    event = EventFactory()
    assert str(event) == event.title


@pytest.mark.django_db
def test_recurring_event_str():
    rec_event = RecurringEventFactory()
    assert str(rec_event) == f'{rec_event.event.title} - {rec_event.get_recurrence_rule_display()}'


@pytest.mark.django_db
def test_calculate_next_occurrence_daily():
    now = timezone.now()
    event = RecurringEventFactory(
        event__start_datetime=now - timedelta(days=1),
        recurrence_rule=RecurringEvent.RecurrenceRule.DAILY
    )
    result = event.calculate_next_occurrence()
    assert result.date() == (now.date())


@pytest.mark.django_db
def test_calculate_next_occurrence_weekly():
    now = timezone.now()
    event = RecurringEventFactory(
        event__start_datetime=now - timedelta(weeks=1),
        recurrence_rule=RecurringEvent.RecurrenceRule.WEEKLY
    )
    result = event.calculate_next_occurrence()
    assert result.date() == (now.date())


@pytest.mark.django_db
def test_calculate_next_occurrence_monthly():
    now = timezone.now()
    event = RecurringEventFactory(
        event__start_datetime=now - timedelta(days=31),
        recurrence_rule=RecurringEvent.RecurrenceRule.MONTHLY
    )
    result = event.calculate_next_occurrence()
    assert result.month in [now.month, now.month + 1]


@pytest.mark.django_db
def test_calculate_next_occurrence_yearly():
    now = timezone.now()
    event = RecurringEventFactory(
        event__start_datetime=now - timedelta(days=366),
        recurrence_rule=RecurringEvent.RecurrenceRule.YEARLY
    )
    result = event.calculate_next_occurrence()
    assert result.year == now.year


@pytest.mark.django_db
def test_calculate_next_occurrence_future_event():
    future_date = timezone.now() + timedelta(days=5)
    event = RecurringEventFactory(
        event__start_datetime=future_date,
        recurrence_rule=RecurringEvent.RecurrenceRule.DAILY
    )
    result = event.calculate_next_occurrence()
    assert result == future_date


@pytest.mark.django_db
def test_calculate_next_occurrence_end_before_next():
    now = timezone.now()
    event = RecurringEventFactory(
        event__start_datetime=now - timedelta(days=1),
        recurrence_rule=RecurringEvent.RecurrenceRule.DAILY,
        recurrence_end_datetime=now
    )
    result = event.calculate_next_occurrence()
    assert result is None


@pytest.mark.django_db
def test_calculate_next_occurrence_invalid_rule():
    now = timezone.now()
    event = RecurringEventFactory(
        event__start_datetime=now - timedelta(days=1),
        recurrence_rule='invalid'
    )
    result = event.calculate_next_occurrence()
    assert result is None
