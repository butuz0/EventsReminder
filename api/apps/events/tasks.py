from .models import RecurringEvent
from celery import shared_task


@shared_task
def update_next_event_occurrence_task(recurring_event_id: str) -> None:
    try:
        recurring_event = RecurringEvent.objects.get(id=recurring_event_id)
    except RecurringEvent.DoesNotExist:
        return

    next_occurrence = recurring_event.calculate_next_occurrence()

    if next_occurrence and next_occurrence > recurring_event.event.start_datetime:
        recurring_event.event.start_datetime = next_occurrence
        recurring_event.event.save(update_fields=['start_datetime'])

        eta = next_occurrence
        update_next_event_occurrence_task.apply_async(args=[recurring_event_id], eta=eta)
