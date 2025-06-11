from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _


def custom_validate_email(email: str):
    try:
        validate_email(email)
    except ValidationError:
        raise ValidationError(_('Enter a valid email address.'))

    if not email.endswith('@kpi.ua'):
        raise ValidationError(_('Enter your corporate @kpi.ua email address.'))


class UserManager(BaseUserManager):
    def _create_user(self, first_name: str, last_name: str, email: str, password: str | None, is_admin: bool = False,
                     **extra_fields):
        if not first_name:
            raise ValueError(_('Users must have a first name.'))
        if not last_name:
            raise ValueError(_('Users must have a last name.'))
        if not email:
            raise ValueError(_('Users must have an email address.'))

        email = self.normalize_email(email)
        if not is_admin:
            custom_validate_email(email)
        else:
            validate_email(email)

        user = self.model(first_name=first_name,
                          last_name=last_name,
                          email=email,
                          **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, first_name: str, last_name: str, email: str, password: str | None = None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(first_name=first_name,
                                 last_name=last_name,
                                 email=email,
                                 password=password,
                                 **extra_fields)

    def create_superuser(self, first_name: str, last_name: str, email: str, password: str | None = None,
                         **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self._create_user(first_name=first_name,
                                 last_name=last_name,
                                 email=email,
                                 password=password,
                                 is_admin=True,
                                 **extra_fields)
