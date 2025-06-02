from django.core.management.base import BaseCommand
from django.utils.timezone import now
from django.db.models import Q
from apps.events.models import RecurringEvent
from apps.events.recurring import reschedule_recurring_event
from celery.result import AsyncResult


class Command(BaseCommand):
    help = 'Reschedule recurring events datetime update'

    def handle(self, *args, **kwargs):
        events = RecurringEvent.objects.filter(
            Q(recurrence_end_datetime__gt=now()) | Q(recurrence_end_datetime__isnull=True)
        )

        if not events.exists():
            self.stdout.write(self.style.SUCCESS('No recurring events found.'))
            return

        rescheduled = 0
        for e in events:
            reschedule_recurring_event(e)
            rescheduled += 1

        self.stdout.write(self.style.SUCCESS(
            f'{rescheduled} event(s) rescheduled.'
        ))
