from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware
from apps.users.tests.factories import UserFactory
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
def mock_request():
    request = RequestFactory().get('/')
    SessionMiddleware(lambda req: None).process_request(request)
    AuthenticationMiddleware(lambda req: None).process_request(request)
    request.session.save()
    return request
