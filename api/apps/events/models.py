from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.teams.models import Team
from apps.common.models import TimeStampedModel
from apps.common.validators import image_validator
from apps.common.uploads import upload_event_image
from taggit.managers import TaggableManager
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta

User = get_user_model()


class Event(TimeStampedModel):
    class Priority(models.IntegerChoices):
        LOW = 1, _('Low')
        MEDIUM = 2, _('Medium')
        HIGH = 3, _('High')
        CRITICAL = 4, _('Critical')

    # Required fields
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events',
                                   verbose_name=_('Created By'))
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    start_datetime = models.DateTimeField(verbose_name=_('Start Time'))

    # Optional fields
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='events', null=True, blank=True,
                             verbose_name=_('Team'))
    assigned_to = models.ManyToManyField(User, related_name='assigned_events', verbose_name=_('Assigned To'),
                                         blank=True)
    description = models.TextField(blank=True, verbose_name=_('Description'))
    location = models.CharField(max_length=255, blank=True, verbose_name=_('Location'))
    link = models.URLField(blank=True, null=True, verbose_name=_('Event Link'))
    priority = models.PositiveSmallIntegerField(choices=Priority.choices, default=Priority.MEDIUM,
                                                verbose_name=_('Priority'))
    image = models.ImageField(upload_to=upload_event_image, validators=[image_validator], blank=True, null=True,
                              verbose_name=_('Image'))
    tags = TaggableManager(blank=True, verbose_name=_('Tags'))

    # If event is recurring, RecurringEvent model will be created
    is_recurring = models.BooleanField(default=False, verbose_name=_('Is Recurring'))

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        ordering = ['start_datetime']

    def __str__(self) -> str:
        return self.title


class RecurringEvent(TimeStampedModel):
    '''
    Extends Event model with additional fields for recurring events.
    '''

    class RecurrenceRule(models.TextChoices):
        DAILY = 'd', _('Daily')
        WEEKLY = 'w', _('Weekly')
        MONTHLY = 'm', _('Monthly')
        YEARLY = 'y', _('Yearly')

    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name='recurring_event',
                                 verbose_name=_('Recurring Event'))
    recurrence_rule = models.CharField(verbose_name=_('Recurrence Rule'), max_length=10, choices=RecurrenceRule.choices,
                                       default=RecurrenceRule.WEEKLY)
    recurrence_end_datetime = models.DateTimeField(null=True, blank=True, verbose_name=_('End time'))

    # celery task for updating event.start_datetime
    celery_task_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = _('Recurring Event')
        verbose_name_plural = _('Recurring Events')

    def __str__(self) -> str:
        return f'{self.event.title} - {self.get_recurrence_rule_display()}'

    def calculate_next_occurrence(self) -> datetime | None:
        '''
        Calculate the next occurrence of the event based on the recurrence rule.
        Returns None if:
            - recurrence is finished (next occurrence > end_datetime);
            - recurrence rule is unrecognized.
        '''
        event_datetime = self.event.start_datetime

        if timezone.is_naive(event_datetime):
            event_datetime = timezone.make_aware(event_datetime)

        if event_datetime > timezone.now():
            return event_datetime

        if self.recurrence_rule == self.RecurrenceRule.DAILY:
            next_occurrence = event_datetime + timedelta(days=1)
        elif self.recurrence_rule == self.RecurrenceRule.WEEKLY:
            next_occurrence = event_datetime + timedelta(weeks=1)
        elif self.recurrence_rule == self.RecurrenceRule.MONTHLY:
            next_occurrence = event_datetime + relativedelta(months=1)
        elif self.recurrence_rule == self.RecurrenceRule.YEARLY:
            next_occurrence = event_datetime + relativedelta(years=1)
        else:
            return None

        if self.recurrence_end_datetime and next_occurrence > self.recurrence_end_datetime:
            return None
        return next_occurrence
