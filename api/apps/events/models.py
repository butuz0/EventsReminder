from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from apps.common.models import TimeStampedModel
from taggit.managers import TaggableManager
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
import magic
import uuid
import os

User = get_user_model()

ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif']
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB


def validate_image_type(value):
    mime_type = magic.Magic(mime=True).from_buffer(value.read(2048))
    if mime_type not in ALLOWED_IMAGE_TYPES:
        raise ValidationError(_(f'Unsupported file type: {mime_type}. Your image must be one of the following: {", ".join(ALLOWED_IMAGE_TYPES)}.'))


def validate_image_size(value):  
    if value.size > MAX_IMAGE_SIZE:
        raise ValidationError(_('File is too large. Max size: 5MB.'))


def upload_to(instance, filename):
    extension = os.path.splitext(filename)[1]
    return os.path.join('event_images/', f'{uuid.uuid4()}{extension}')


class Event(TimeStampedModel):
    class Priority(models.TextChoices):
        LOW = 'low', _('Low')
        MEDIUM = 'medium', _('Medium')
        HIGH = 'high', _('High')
        CRITICAL = 'critical', _('Critical')

    # Required fields
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events', verbose_name=_('Created By'))
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    start_datetime = models.DateTimeField(verbose_name=_('Start Time'))

    # Optional fields
    assigned_to = models.ManyToManyField(User, related_name='assigned_events', verbose_name=_('Assigned To'), blank=True)
    description = models.TextField(blank=True, verbose_name=_('Description'))
    location = models.CharField(max_length=255, blank=True, verbose_name=_('Location'))
    link = models.URLField(blank=True, null=True, verbose_name=_('Event Link'))
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM, verbose_name=_('Priority'))
    image = models.ImageField(upload_to=upload_to, validators=[validate_image_type, validate_image_size], blank=True, null=True, verbose_name=_('Image'))
    tags = TaggableManager(blank=True, verbose_name=_('Tags'))

    # If event is recurring, RecurringEvent model will be created
    is_recurring = models.BooleanField(default=False, verbose_name=_('Is Recurring'))

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        ordering = ['-start_datetime']
    
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
    
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name='recurring_event', verbose_name=_('Recurring Event'))
    recurrence_rule = models.CharField(verbose_name=_('Recurrence Rule'), max_length=10, choices=RecurrenceRule.choices, default=RecurrenceRule.WEEKLY)
    recurrence_end_datetime = models.DateTimeField(null=True, blank=True, verbose_name=_('End time'))
    next_occurrence = models.DateTimeField(null=True, blank=True, verbose_name=_('Next Occurrence'))
    last_occurrence = models.DateTimeField(null=True, blank=True, verbose_name=_('Last Occurrence'))

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
            - last_occurrence is missing (event has not occurred yet);
            - recurrence rule is unrecognized.
        '''
        if not self.last_occurrence:
            return self.next_occurrence

        next_occurrence = None
        
        if self.recurrence_rule == self.RecurrenceRule.DAILY:
            next_occurrence = self.last_occurrence + timedelta(days=1)
        elif self.recurrence_rule == self.RecurrenceRule.WEEKLY:
            next_occurrence = self.last_occurrence + timedelta(weeks=1)
        elif self.recurrence_rule == self.RecurrenceRule.MONTHLY:
            next_occurrence = self.last_occurrence + relativedelta(months=1)
        elif self.recurrence_rule == self.RecurrenceRule.YEARLY:
            next_occurrence = self.last_occurrence + relativedelta(years=1)
        else:
            return None
    
        if self.recurrence_end_datetime and next_occurrence > self.recurrence_end_datetime:
            return None
        return next_occurrence
