from apps.profiles.serializers import (
    ProfileRetrieveSerializer,
    ProfileUpdateSerializer,
    TelegramDataSerializer,
    ProfileSetupSerializer
)
from apps.profiles.tests.factories import (
    ProfileFactory,
    TelegramDataFactory,
    ProfileWithTelegramFactory
)
from apps.units.tests.factories import DepartmentFactory, FacultyFactory
from unittest.mock import Mock
import pytest


@pytest.fixture
def profile_with_telegram():
    return ProfileWithTelegramFactory()


@pytest.fixture
def request_context(rf):
    return rf.get('/fake-request')


@pytest.mark.django_db
def test_profile_retrieve_serializer(profile_with_telegram, request_context):
    profile = ProfileWithTelegramFactory()
    serializer = ProfileRetrieveSerializer(profile, context={'request': request_context})
    data = serializer.data

    assert 'id' in data
    assert 'email' in data

    assert 'department_name' in data
    assert 'department_abbreviation' in data
    assert data['department_name'] == profile.department.department_name
    assert data['department_abbreviation'] == profile.department.department_abbreviation

    assert 'faculty_name' in data
    assert 'faculty_abbreviation' in data
    assert data['faculty_name'] == profile.department.faculty.faculty_name
    assert data['faculty_abbreviation'] == profile.department.faculty.faculty_abbreviation

    assert 'telegram' in data
    assert data['telegram']['telegram_username'] == profile.telegram.telegram_username


@pytest.mark.django_db
def test_profile_retrieve_serializer_no_department(profile_with_telegram, request_context):
    profile = ProfileWithTelegramFactory(department=None)
    serializer = ProfileRetrieveSerializer(profile, context={'request': request_context})
    data = serializer.data

    assert 'department_name' in data
    assert 'department_abbreviation' in data
    assert data['department_name'] is None
    assert data['department_abbreviation'] is None

    assert 'faculty_name' in data
    assert 'faculty_abbreviation' in data
    assert data['faculty_name'] is None
    assert data['faculty_abbreviation'] is None


@pytest.mark.django_db
def test_profile_update_serializer():
    department = DepartmentFactory()
    profile = ProfileFactory(department=department)
    data = {
        'first_name': 'New first name',
        'last_name': 'New last name',
        'position': 'New position',
        'department': department.id,
    }

    serializer = ProfileUpdateSerializer(profile,
                                         data=data,
                                         partial=True)
    assert serializer.is_valid()

    instance = serializer.save()

    assert instance.user.first_name == 'New first name'
    assert instance.user.last_name == 'New last name'
    assert instance.position == 'New position'
    assert instance.department == department


@pytest.mark.django_db
def test_telegram_data_serializer():
    telegram_data = TelegramDataFactory()
    serializer = TelegramDataSerializer(telegram_data)
    data = serializer.data

    assert data['telegram_username'] == telegram_data.telegram_username
    assert data['is_verified'] is True


@pytest.mark.django_db
def test_profile_setup_serializer():
    profile = ProfileFactory()

    department = DepartmentFactory()
    data = {
        'position': 'New position',
        'department': department.id
    }

    serializer = ProfileSetupSerializer(profile, data=data)
    assert serializer.is_valid()

    instance = serializer.save()

    assert instance.position == 'New position'
    assert instance.department == department


@pytest.mark.django_db
def test_profile_retrieve_serializer_avatar_url(request_context):
    profile = ProfileFactory()
    serializer = ProfileRetrieveSerializer(profile, context={'request': request_context})
    data = serializer.data

    assert data['avatar_url'] == request_context.build_absolute_uri(profile.avatar.url)


@pytest.mark.django_db
def test_profile_retrieve_serializer_avatar_url_local(request_context):
    profile = ProfileFactory()
    mocked_request = Mock()
    mocked_request.build_absolute_uri.return_value = 'http://localhost/media/avatar.jpg'

    serializer = ProfileRetrieveSerializer(profile, context={'request': mocked_request})
    data = serializer.data

    assert data['avatar_url'] == 'http://localhost:8080/media/avatar.jpg'


@pytest.mark.django_db
def test_profile_retrieve_serializer_no_avatar_url(request_context):
    profile = ProfileFactory(avatar=None)
    serializer = ProfileRetrieveSerializer(profile, context={'request': request_context})
    data = serializer.data

    assert data['avatar_url'] is None
