from apps.users.tests.factories import UserFactory
from rest_framework.test import APIClient
from pytest_factoryboy import register
import pytest

register(UserFactory)


@pytest.fixture
def normal_user(db, user_factory):
    new_user = user_factory.create()
    return new_user


@pytest.fixture
def super_user(db, user_factory):
    new_user = user_factory.create(is_superuser=True, is_staff=True)
    return new_user


@pytest.fixture
def client(normal_user):
    def _auth_client(user=None):
        client = APIClient()
        client.force_authenticate(user=user or normal_user)
        return client

    return _auth_client
