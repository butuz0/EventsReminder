from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import pytest

User = get_user_model()


@pytest.mark.django_db
def test_create_normal_user(normal_user):
    assert normal_user.email is not None
    assert normal_user.first_name is not None
    assert normal_user.last_name is not None
    assert normal_user.password is not None
    assert normal_user.pkid is not None
    assert normal_user.is_active
    assert not normal_user.is_staff
    assert not normal_user.is_superuser


@pytest.mark.django_db
def test_create_superuser(super_user):
    assert super_user.email is not None
    assert super_user.first_name is not None
    assert super_user.last_name is not None
    assert super_user.password is not None
    assert super_user.pkid is not None
    assert super_user.is_active
    assert super_user.is_staff
    assert super_user.is_superuser


@pytest.mark.django_db
def test_full_name(normal_user):
    full_name = normal_user.full_name
    expected_full_name = f'{normal_user.first_name.title()} {normal_user.last_name.title()}'
    assert full_name == expected_full_name


@pytest.mark.django_db
def test_update_user(normal_user):
    new_first_name = 'Peter'
    new_last_name = 'Parker'
    normal_user.first_name = new_first_name
    normal_user.last_name = new_last_name
    normal_user.save()

    updated_user = User.objects.get(pk=normal_user.pk)
    assert updated_user.first_name == new_first_name
    assert updated_user.last_name == new_last_name


@pytest.mark.django_db
def test_delete_user(normal_user):
    user_pk = normal_user.pk
    normal_user.delete()

    with pytest.raises(User.DoesNotExist):
        User.objects.get(pk=user_pk)


@pytest.mark.django_db
def test_user_str(normal_user):
    assert str(normal_user) == f'{normal_user.first_name.title()} {normal_user.last_name.title()}'


@pytest.mark.django_db
def test_user_email_normalized(normal_user):
    email = normal_user.email
    assert email == email.lower()


@pytest.mark.django_db
def test_user_email_incorrect(user_factory):
    with pytest.raises(ValidationError) as err:
        user_factory.create(email='mail.com')
    assert err.value.messages[0] == 'Enter a valid email address.'


@pytest.mark.django_db
def test_normal_user_email_not_corporate(user_factory):
    with pytest.raises(ValidationError) as err:
        user_factory.create(email='email@gmail.com')
    assert err.value.messages[0] == 'Enter your corporate @kpi.ua email address.'


@pytest.mark.django_db
def test_create_user_with_no_email(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(email=None)
    assert str(err.value) == 'Users must have an email address.'


@pytest.mark.django_db
def test_create_user_with_no_first_name(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(first_name=None)
    assert str(err.value) == 'Users must have a first name.'


@pytest.mark.django_db
def test_create_user_with_no_last_name(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(last_name=None)
    assert str(err.value) == 'Users must have a last name.'


@pytest.mark.django_db
def test_super_user_is_not_staff(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(is_superuser=True, is_staff=False)
    assert str(err.value) == 'Superuser must have is_staff=True.'


@pytest.mark.django_db
def test_super_user_is_not_superuser(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(is_superuser=False, is_staff=True)
    assert str(err.value) == 'Superuser must have is_superuser=True.'
