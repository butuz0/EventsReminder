from django.core.exceptions import ValidationError
from apps.registration_cards.tests.factories import RegistrationCardFactory
import pytest


@pytest.mark.django_db
def test_registration_card_str():
    card = RegistrationCardFactory()
    assert str(card) == card.organization_name


@pytest.mark.django_db
def test_registration_card_valid_edrpou():
    card = RegistrationCardFactory.build(edrpou_code='12345678')
    card.clean()
    assert card.edrpou_code == '12345678'


@pytest.mark.django_db
def test_registration_card_invalid_edrpou_non_digits():
    card = RegistrationCardFactory.build(edrpou_code='abc12345')

    with pytest.raises(ValidationError) as e:
        card.clean()

    assert 'edrpou_code' in e.value.message_dict
    assert e.value.message_dict['edrpou_code'][0] == 'EDRPOU Code must contain only digits.'


@pytest.mark.django_db
def test_registration_card_invalid_edrpou_length():
    card = RegistrationCardFactory.build(edrpou_code='1234')

    with pytest.raises(ValidationError) as e:
        card.clean()

    assert 'edrpou_code' in e.value.message_dict
    assert e.value.message_dict['edrpou_code'][0] == 'EDRPOU Code must be 8 digits long.'
