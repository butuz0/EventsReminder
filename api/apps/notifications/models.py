from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from apps.events.models import Event

User = get_user_model()


class Notification(models.Model):
    class NotificationMethod(models.TextChoices):
        EMAIL = 'email', _('Email')
        TELEGRAM = 'tg', _('Telegram')

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='notifications', verbose_name=_('Event'))
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications',
                                   verbose_name=_('Created By'))
    notification_method = models.CharField(max_length=10, choices=NotificationMethod.choices,
                                           default=NotificationMethod.EMAIL, verbose_name=_('Notification Method'))
    notification_datetime = models.DateTimeField(verbose_name=_('Notification Datetime'))
    celery_task_id = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Celery Task ID'))
    is_sent = models.BooleanField(default=False, blank=True, verbose_name=_('Is Sent'))

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        ordering = ['-notification_datetime']

    def __str__(self) -> str:
        return f'{self.event.title} - {self.get_notification_method_display()}'
