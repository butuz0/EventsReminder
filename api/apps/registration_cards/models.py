from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from apps.common.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField
from encrypted_model_fields.fields import EncryptedCharField

User = get_user_model()


class RegistrationCard(TimeStampedModel):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Created By'))

    # Legal Entity
    organization_name = models.CharField(max_length=255, verbose_name=_('Full Organization Name'))
    edrpou_code = models.CharField(max_length=8, verbose_name=_('EDRPOU Code'))
    region = models.CharField(max_length=100, blank=True, verbose_name=_('Region'))
    city = models.CharField(max_length=100, blank=True, verbose_name=_('City'))

    # Applicant
    full_name = EncryptedCharField(max_length=255, blank=True, verbose_name=_('Applicant Full Name'))
    id_number = EncryptedCharField(max_length=20, blank=True, verbose_name=_('IPN or series/number of document'))
    keyword_phrase = EncryptedCharField(max_length=255, blank=True, verbose_name=_('Keyword Phrase'))
    voice_phrase = EncryptedCharField(max_length=255, blank=True, verbose_name=_('Voice Phrase'))

    # Contacts
    email = models.EmailField(blank=True, verbose_name=_('Email'))
    phone_number = PhoneNumberField(max_length=20, blank=True, verbose_name=_('Phone Number'))

    # Electronic Seal
    electronic_seal_name = EncryptedCharField(max_length=255, blank=True,
                                              verbose_name=_('Electronic Seal Name'))
    electronic_seal_keyword_phrase = EncryptedCharField(max_length=255, blank=True,
                                                        verbose_name=_('Electronic Seal Keyword Phrase'))

    class Meta:
        verbose_name = 'Registration Card'
        verbose_name_plural = 'Registration Cards'

    def __str__(self):
        return self.organization_name

    def clean(self):
        if self.edrpou_code and not self.edrpou_code.isdigit():
            raise ValidationError({'edrpou_code': _('Код ЄДРПОУ повинен містити лише цифри.')})
        if self.edrpou_code and len(self.edrpou_code) != 8:
            raise ValidationError({'edrpou_code': _('Код ЄДРПОУ повинен складатись із 8-ми цифр.')})
