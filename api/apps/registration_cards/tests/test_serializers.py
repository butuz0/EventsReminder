from apps.registration_cards.serializers import RegistrationCardSerializer
from apps.users.tests.factories import UserFactory
import pytest


@pytest.mark.django_db
def test_registration_card_serializer_valid_data():
    user = UserFactory()
    data = {
        'organization_name': 'Test',
        'edrpou_code': '12345678',
        'region': 'Kyivska',
        'city': 'Kyiv',
        'full_name': 'Peter Parker',
        'id_number': '12345678',
        'keyword_phrase': 'Keyword phrase',
        'voice_phrase': 'Voice phrase',
        'email': 'test@gmail.com',
        'phone_number': '+380999999999',
        'electronic_seal_name': 'Seal name',
        'electronic_seal_keyword_phrase': 'Seal keyword',
    }

    serializer = RegistrationCardSerializer(data=data)
    assert serializer.is_valid()

    instance = serializer.save(created_by=user)
    assert instance.organization_name == data['organization_name']
    assert instance.created_by == user


@pytest.mark.django_db
def test_registration_card_serializer_edrpou_non_digits():
    data = {
        'organization_name': 'Test',
        'edrpou_code': 'ABC12345'
    }
    serializer = RegistrationCardSerializer(data=data)

    assert not serializer.is_valid()
    assert 'edrpou_code' in serializer.errors


@pytest.mark.django_db
def test_registration_card_serializer_edrpou_wrong_length():
    data = {
        'organization_name': 'Test',
        'edrpou_code': '1234'
    }
    serializer = RegistrationCardSerializer(data=data)

    assert not serializer.is_valid()
    assert 'edrpou_code' in serializer.errors
