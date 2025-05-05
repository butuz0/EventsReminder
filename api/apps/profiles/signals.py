from django.db.models.signals import post_save
from django.dispatch import receiver
from config.settings.base import AUTH_USER_MODEL
from django.db.models.base import Model
from .models import Profile, TelegramData
from typing import Any, Type


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_profile(sender: Type[Model], instance: Model, created: bool, **kwargs: Any) -> None:
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Profile)
def create_telegram_data_model(sender, instance: Profile, created: bool, **kwargs):
    if created and not hasattr(instance, 'telegram'):
        TelegramData.objects.create(profile=instance)
