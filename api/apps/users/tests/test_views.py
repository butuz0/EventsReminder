import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_custom_token_obtain_pair_sets_cookies(user_factory):
    user = user_factory.create(password='Pass123456')
    client = APIClient()

    response = client.post(
        reverse('login'),
        {'email': user.email, 'password': 'Pass123456'},
        format='json'
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.cookies.get('access') is not None
    assert response.cookies.get('refresh') is not None
    assert response.cookies.get('logged_in') is not None
    assert response.data.get('message') == 'Login Successful.'


@pytest.mark.django_db
def test_token_refresh_sets_new_tokens(user_factory):
    user = user_factory.create(password='Pass123456')
    client = APIClient()

    login_response = client.post(
        reverse('login'),
        {'email': user.email, 'password': 'Pass123456'},
        format='json'
    )

    refresh_token = login_response.cookies['refresh'].value
    client.cookies['refresh'] = refresh_token

    response = client.post(reverse('refresh'))

    assert response.status_code == status.HTTP_200_OK
    assert response.data.get('message') == 'Access tokens refreshed successfully.'
