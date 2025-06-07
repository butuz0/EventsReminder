from apps.users.forms import UserCreationForm
from apps.users.tests.factories import UserFactory
import pytest


@pytest.mark.django_db
def test_user_creation_form_valid_data():
    data = {
        'email': 'test_email@kpi.ua',
        'first_name': 'Peter',
        'last_name': 'Parker',
        'password1': 'Pass123456',
        'password2': 'Pass123456',
    }
    form = UserCreationForm(data)
    assert form.is_valid()


@pytest.mark.django_db
def test_user_creation_form_invalid_data():
    user = UserFactory()
    data = {
        'email': user.email,
        'first_name': 'Peter',
        'last_name': 'Parker',
        'password1': 'Pass123456',
        'password2': 'Pass123456',
    }
    form = UserCreationForm(data)
    assert not form.is_valid()
    assert form.errors['email'] == ['A user with this email already exists.']
