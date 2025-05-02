from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RegistrationCardsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.registration_cards'
    verbose_name = _('Registration Cards')
