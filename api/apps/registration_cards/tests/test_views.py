from django.urls import reverse
from apps.registration_cards.tests.factories import RegistrationCardFactory
from apps.registration_cards.models import RegistrationCard
from rest_framework.test import APIClient
import pytest


@pytest.mark.django_db
def test_create_registration_card(normal_user):
    client = APIClient()
    client.force_authenticate(user=normal_user)

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
    response = client.post(
        reverse('registration-card-list-create'),
        data=data,
        format='json'
    )

    assert response.status_code == 201
    assert RegistrationCard.objects.filter(created_by=normal_user).exists()


@pytest.mark.django_db
def test_list_registration_cards(normal_user):
    RegistrationCardFactory.create_batch(3, created_by=normal_user)
    RegistrationCardFactory.create_batch(2)
    client = APIClient()
    client.force_authenticate(user=normal_user)

    response = client.get(reverse('registration-card-list-create'))

    assert response.status_code == 200
    assert len(response.data['results']) == 3


@pytest.mark.django_db
def test_retrieve_registration_card(normal_user):
    card = RegistrationCardFactory(created_by=normal_user)
    client = APIClient()
    client.force_authenticate(user=normal_user)

    response = client.get(
        reverse(
            'registration-card-retrieve-update',
            kwargs={'id': card.id}
        )
    )

    assert response.status_code == 200
    assert response.data['id'] == str(card.id)


@pytest.mark.django_db
def test_delete_registration_card(normal_user):
    card = RegistrationCardFactory(created_by=normal_user)
    client = APIClient()
    client.force_authenticate(user=normal_user)

    response = client.delete(
        reverse(
            'registration-card-retrieve-update',
            kwargs={'id': card.id}
        )
    )

    assert response.status_code == 204
    assert not RegistrationCard.objects.filter(id=card.id).exists()
