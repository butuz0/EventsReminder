from .models import RecurringEvent
from .tasks import update_next_event_occurrence_task
from celery.result import AsyncResult


def reschedule_recurring_event(recurring_event: RecurringEvent) -> None:
    """
    Creates a celery task for updating the next occurrence of
    a recurring event. Deletes an old celery task if it exists.
    """
    if recurring_event.celery_task_id:
        AsyncResult(recurring_event.celery_task_id).revoke(terminate=True)

    eta = recurring_event.calculate_next_occurrence()
    if eta:
        task = update_next_event_occurrence_task.apply_async(args=[recurring_event.id], eta=eta)
        recurring_event.celery_task_id = task.id

        # save a new celery task id, avoiding post_save signal recursion
        RecurringEvent.objects.filter(id=recurring_event.id).update(celery_task_id=task.id)
