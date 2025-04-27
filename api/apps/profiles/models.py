from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField
from apps.common.models import TimeStampedModel
from apps.units.models import Department

User = get_user_model()


class Profile(TimeStampedModel):
    class Gender(models.TextChoices):
        MALE = 'm', _('Male')
        FEMALE = 'f', _('Female')
        OTHER = 'o', _('Other')
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, related_name='employees', null=True)
    position = models.CharField(verbose_name=_('Position'), max_length=250, null=True)
    gender = models.CharField(verbose_name=_('Gender'), max_length=10, choices=Gender.choices, default=Gender.OTHER)
    phone_number = PhoneNumberField(verbose_name=_('Phone Number'), max_length=20, unique=True, null=True)
    telegram_username = models.CharField(verbose_name=_('Telegram Username'), max_length=50, null=True, unique=True, blank=True)
    telegram_phone_number = PhoneNumberField(verbose_name=_('Telegram Phone Number'), max_length=20, null=True, unique=True, blank=True)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
        
        indexes = [
            models.Index(fields=['telegram_username']),
            models.Index(fields=['telegram_phone_number']),
        ]
    
    def __str__(self):
        return f'{self.user.full_name} - {self.position}'
