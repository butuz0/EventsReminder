from .factories import NotificationFactory
from rest_framework.test import APIRequestFactory
from apps.notifications.permissions import IsOwner
from apps.events.tests.factories import EventFactory
from apps.profiles.tests.factories import UserWithProfileFactory
import pytest


@pytest.mark.django_db
def test_notification_is_owner_permission_granted(normal_user):
    event = EventFactory(created_by=normal_user)
    notification = NotificationFactory(event=event, created_by=normal_user)

    factory = APIRequestFactory()
    request = factory.get('/')
    request.user = normal_user

    permission = IsOwner()

    assert permission.has_object_permission(request, view=None, obj=notification)


@pytest.mark.django_db
def test_notification_is_owner_permission_denied(normal_user):
    other_user = UserWithProfileFactory()
    event = EventFactory(created_by=other_user)
    notification = NotificationFactory(event=event, created_by=other_user)

    factory = APIRequestFactory()
    request = factory.get('/')
    request.user = normal_user

    permission = IsOwner()

    assert not permission.has_object_permission(request, view=None, obj=notification)
