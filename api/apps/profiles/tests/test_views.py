from django.conf import settings
from django.urls import reverse
from django.utils.timezone import now
from apps.units.tests.factories import DepartmentFactory
from apps.profiles.tests.factories import UserWithProfileFactory, ProfileFactory
from apps.profiles.models import TelegramData, Profile
from rest_framework.test import APIClient
import pytest
import hashlib
import hmac


@pytest.mark.django_db
def test_profile_list_api_view(super_user):
    user = UserWithProfileFactory()
    ProfileFactory(user=super_user)
    other_profiles = ProfileFactory.create_batch(3)

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get(reverse('profile-list'))
    assert response.status_code == 200

    returned_ids = [item['id'] for item in response.data['results']]
    assert all(str(profile.user.id) in returned_ids for profile in other_profiles)
    assert str(user.id) not in returned_ids
    assert str(super_user.id) not in returned_ids


@pytest.mark.django_db
def test_profile_detail_view():
    user = UserWithProfileFactory()
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get(reverse('profile-detail', kwargs={'user_id': user.id}))

    assert response.status_code == 200
    assert response.data['id'] == str(user.id)


@pytest.mark.django_db
def test_my_profile_view(normal_user):
    client = APIClient()
    client.force_authenticate(user=normal_user)

    response = client.get(reverse('my-profile'))

    assert response.status_code == 200
    assert response.data['id'] == str(normal_user.id)


@pytest.mark.django_db
def test_profile_update_view():
    dep1 = DepartmentFactory()
    dep2 = DepartmentFactory()
    user = UserWithProfileFactory(
        first_name='Old first name',
        profile__position='Old position',
        profile__department=dep1
    )

    client = APIClient()
    client.force_authenticate(user=user)

    data = {
        'first_name': 'New first name',
        'position': 'New position',
        'department': dep2.id
    }
    response = client.patch(reverse('profile-update'),
                            data=data,
                            format='json')

    assert response.status_code == 200

    user.refresh_from_db()
    assert user.first_name == 'New first name'
    assert user.profile.position == 'New position'
    assert user.profile.department == dep2


@pytest.mark.django_db
def test_profile_setup_view_success(normal_user):
    department = DepartmentFactory()
    client = APIClient()
    client.force_authenticate(user=normal_user)

    data = {
        'position': 'New position',
        'department': department.id
    }
    response = client.put(reverse('my-profile-setup'),
                          data=data,
                          format='json')
    assert response.status_code == 200
    assert response.data['message'] == 'Profile set up successfully'

    assert Profile.objects.filter(user=normal_user).exists()
    assert normal_user.profile.position == 'New position'
    assert normal_user.profile.department == department


@pytest.mark.django_db
def test_profile_setup_view_fail(normal_user):
    client = APIClient()
    client.force_authenticate(user=normal_user)

    data = {
        'position': 'New position',
        'department': 'Fail'
    }
    response = client.put(reverse('my-profile-setup'),
                          data=data,
                          format='json')
    assert response.status_code == 400


def get_telegram_auth_payload() -> dict:
    return {
        'id': 123456,
        'first_name': 'Peter',
        'last_name': 'Parker',
        'username': 'peterparker123',
        'photo_url': 'https://tg/peterparker123.jpg',
        'auth_date': int(now().timestamp())
    }


def get_telegram_auth_payload_with_hash(payload: dict | None = None) -> dict:
    full_payload = get_telegram_auth_payload() if not payload else payload.copy()

    data_check_string = '\n'.join(f'{k}={full_payload[k]}' for k in sorted(full_payload))
    secret_key = hashlib.sha256(settings.TELEGRAM_BOT_TOKEN.encode()).digest()
    full_payload['hash'] = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    return full_payload


@pytest.mark.django_db
def test_telegram_auth_success():
    client = APIClient()
    user = UserWithProfileFactory()
    client.force_authenticate(user=user)

    response = client.post(reverse('telegram-auth'),
                           get_telegram_auth_payload_with_hash(),
                           format='json')

    assert response.status_code == 200
    assert response.data['detail'] == 'Telegram account connected successfully'
    assert TelegramData.objects.filter(profile=user.profile, telegram_user_id=123456).exists()


@pytest.mark.django_db
def test_telegram_auth_expired_date():
    client = APIClient()
    user = UserWithProfileFactory()
    client.force_authenticate(user=user)

    payload = get_telegram_auth_payload()
    payload['auth_date'] = int(now().timestamp() - 600)
    response = client.post(reverse('telegram-auth'),
                           get_telegram_auth_payload_with_hash(payload),
                           format='json')

    assert response.status_code == 403
    assert response.data['detail'] == 'Telegram auth data expired'


@pytest.mark.django_db
def test_telegram_auth_no_hash():
    client = APIClient()
    user = UserWithProfileFactory()
    client.force_authenticate(user=user)

    response = client.post(reverse('telegram-auth'),
                           get_telegram_auth_payload(),
                           format='json')

    assert response.status_code == 400
    assert response.data['detail'] == 'Hash missing'


@pytest.mark.django_db
def test_telegram_auth_invalid_data():
    client = APIClient()
    user = UserWithProfileFactory()
    client.force_authenticate(user=user)

    payload = get_telegram_auth_payload_with_hash()
    payload['username'] = 'invalid'
    response = client.post(reverse('telegram-auth'), payload, format='json')

    assert response.status_code == 403
    assert response.data['detail'] == 'Invalid Telegram auth data'


@pytest.mark.django_db
def test_telegram_auth_requires_authentication():
    client = APIClient()

    response = client.post(reverse('telegram-auth'), {}, format='json')

    assert response.status_code == 401
    assert response.data['detail'] == 'Authentication credentials were not provided.'
