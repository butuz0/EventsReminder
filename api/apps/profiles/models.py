from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from apps.common.models import TimeStampedModel
from apps.common.validators import image_validator
from apps.common.uploads import upload_avatar
from apps.units.models import Department

User = get_user_model()


class Profile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name='employees', null=True)
    position = models.CharField(verbose_name=_('Position'), max_length=250, null=True)
    avatar = models.ImageField(upload_to=upload_avatar, validators=[image_validator], blank=True, null=True,
                               verbose_name=_('Avatar'))

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
        indexes = [
            models.Index(fields=['position']),
        ]

    def __str__(self) -> str:
        return f'{self.user.full_name} - {self.position or 'Unknown position'}'

    def is_telegram_verified(self) -> bool:
        return hasattr(self, 'telegram') and self.telegram.is_verified


class TelegramData(TimeStampedModel):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='telegram')

    # set by telegram login widget
    telegram_username = models.CharField(max_length=50, null=True, unique=True, verbose_name=_('Telegram Username'))
    telegram_first_name = models.CharField(max_length=50, null=True, verbose_name=_('Telegram First Name'))
    telegram_last_name = models.CharField(max_length=50, null=True, verbose_name=_('Telegram Last Name'))
    telegram_user_id = models.BigIntegerField(unique=True, null=True, verbose_name=_('Telegram User Id'))

    # set by telegram bot
    is_verified = models.BooleanField(default=False, verbose_name=_('Is Verified'))

    class Meta:
        verbose_name = _('Telegram Data')
        verbose_name_plural = _('Telegram Data')

    def __str__(self) -> str:
        return self.telegram_username or f'Unconnected user {self.profile.user}'
