from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()

NOTIFICATION_MODELS_LIMIT = {
    'app_label__in': ['events', 'registration_cards'],
    'model__in': ['event', 'registrationcard']
}


class Notification(models.Model):
    class NotificationMethod(models.TextChoices):
        EMAIL = 'email', _('Email')
        TELEGRAM = 'tg', _('Telegram')

    # Generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     limit_choices_to=NOTIFICATION_MODELS_LIMIT, verbose_name=_('Content Type'))
    object_id = models.UUIDField(verbose_name=_('Object ID'))
    content_object = GenericForeignKey('content_type', 'object_id')

    # Notification data
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
        return f'{self.content_object} – {self.get_notification_method_display()}'
