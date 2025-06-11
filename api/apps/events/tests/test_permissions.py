from .factories import EventFactory, RecurringEventFactory
from apps.events.permissions import IsOwner, IsOwnerOrAssignedTo
from apps.users.tests.factories import UserFactory
from rest_framework.test import APIRequestFactory
import pytest


@pytest.mark.django_db
def test_event_is_owner_permission_granted(normal_user):
    event = EventFactory(created_by=normal_user)
    request = APIRequestFactory().get('/')
    request.user = normal_user
    permission = IsOwner()

    assert permission.has_object_permission(request, view=None, obj=event) is True


@pytest.mark.django_db
def test_event_is_owner_permission_denied(normal_user):
    other_user = UserFactory()
    event = EventFactory(created_by=other_user)
    request = APIRequestFactory().get('/')
    request.user = normal_user
    permission = IsOwner()

    assert permission.has_object_permission(request, view=None, obj=event) is False


@pytest.mark.django_db
def test_recurring_event_is_owner_permission_granted(normal_user):
    event = EventFactory(created_by=normal_user)
    recurring = RecurringEventFactory(event=event)

    request = APIRequestFactory().get('/')
    request.user = normal_user
    permission = IsOwner()

    assert permission.has_object_permission(request, view=None, obj=recurring) is True


@pytest.mark.django_db
def test_event_is_owner_permission_admin(super_user):
    event = EventFactory()
    request = APIRequestFactory().get('/')
    request.user = super_user
    permission = IsOwner()

    assert permission.has_object_permission(request, view=None, obj=event) is True


@pytest.mark.django_db
def test_is_owner_or_assigned_permission_granted_owner(normal_user):
    event = EventFactory(created_by=normal_user)
    request = APIRequestFactory().get('/')
    request.user = normal_user
    permission = IsOwnerOrAssignedTo()

    assert permission.has_object_permission(request, view=None, obj=event) is True


@pytest.mark.django_db
def test_is_owner_or_assigned_permission_granted_assigned(normal_user):
    event = EventFactory(assigned_to=[normal_user])
    request = APIRequestFactory().get('/')
    request.user = normal_user
    permission = IsOwnerOrAssignedTo()

    assert permission.has_object_permission(request, view=None, obj=event) is True


@pytest.mark.django_db
def test_is_owner_or_assigned_permission_denied(normal_user):
    event = EventFactory()
    request = APIRequestFactory().get('/')
    request.user = normal_user
    permission = IsOwnerOrAssignedTo()

    assert permission.has_object_permission(request, view=None, obj=event) is False


@pytest.mark.django_db
def test_is_owner_or_assigned_permission_admin(super_user):
    event = EventFactory()
    request = APIRequestFactory().get('/')
    request.user = super_user
    permission = IsOwnerOrAssignedTo()

    assert permission.has_object_permission(request, view=None, obj=event) is True
