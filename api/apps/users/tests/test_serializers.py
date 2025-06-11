import pytest
from django.contrib.auth import get_user_model
from apps.users.serializers import CreateUserSerializer

User = get_user_model()


@pytest.mark.django_db
def test_create_user_serializer_valid():
    data = {
        'email': 'peter@kpi.ua',
        'first_name': 'Peter',
        'last_name': 'Parker',
        'password': 'Pass123456'
    }

    serializer = CreateUserSerializer(data=data)
    assert serializer.is_valid(), serializer.errors

    user = serializer.save()
    assert isinstance(user, User)
    assert user.first_name == 'Peter'
    assert user.check_password('Pass123456')


@pytest.mark.django_db
def test_create_user_serializer_missing_fields():
    data = {
        'first_name': 'Peter'
    }
    serializer = CreateUserSerializer(data=data)
    assert not serializer.is_valid()
    assert 'email' in serializer.errors
    assert 'last_name' in serializer.errors
    assert 'password' in serializer.errors
