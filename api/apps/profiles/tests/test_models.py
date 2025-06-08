from .factories import TelegramDataFactory, ProfileFactory
from apps.profiles.models import TelegramData
import pytest


@pytest.mark.django_db
def test_telegram_data_str():
    telegram_data = TelegramDataFactory()
    assert str(telegram_data) == telegram_data.telegram_username


@pytest.mark.django_db
def test_telegram_data_str_unconnected():
    telegram_data = TelegramDataFactory(telegram_username=None)
    full_name = telegram_data.profile.user.full_name
    assert str(telegram_data) == f'Unconnected user {full_name}'


@pytest.mark.django_db
def test_telegram_data_profile_delete():
    telegram_data = TelegramDataFactory()
    profile = telegram_data.profile

    assert TelegramData.objects.filter(id=telegram_data.id).exists()

    profile.delete()
    assert not TelegramData.objects.filter(id=telegram_data.id).exists()


@pytest.mark.django_db
def test_profile_str_with_position():
    profile = ProfileFactory()
    assert str(profile) == f'{profile.user.full_name} - {profile.position}'


@pytest.mark.django_db
def test_profile_str_without_position():
    profile = ProfileFactory(position=None)
    assert str(profile) == f'{profile.user.full_name} - Unknown position'


@pytest.mark.django_db
def test_profile_is_telegram_verified_true():
    telegram_data = TelegramDataFactory()
    profile = telegram_data.profile
    assert profile.is_telegram_verified() is True


@pytest.mark.django_db
def test_profile_is_telegram_verified_false():
    telegram_data = TelegramDataFactory(is_verified=False)
    profile = telegram_data.profile
    assert profile.is_telegram_verified() is False
