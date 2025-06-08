from apps.registration_cards.permissions import IsOwner
from apps.registration_cards.views import RegistrationCardAPIView
from apps.registration_cards.tests.factories import RegistrationCardFactory
from apps.users.tests.factories import UserFactory
from rest_framework.test import APIRequestFactory
import pytest


@pytest.mark.django_db
def test_is_owner_permission_granted(normal_user):
    card = RegistrationCardFactory(created_by=normal_user)

    request = APIRequestFactory().get('/')
    request.user = normal_user
    view = RegistrationCardAPIView()

    permission = IsOwner()
    assert permission.has_object_permission(request, view, card) is True


@pytest.mark.django_db
def test_is_owner_permission_denied(normal_user):
    another_user = UserFactory()
    card = RegistrationCardFactory(created_by=another_user)

    request = APIRequestFactory().get('/')
    request.user = normal_user
    view = RegistrationCardAPIView()

    permission = IsOwner()
    assert permission.has_object_permission(request, view, card) is False
