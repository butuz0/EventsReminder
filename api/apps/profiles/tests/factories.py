from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from apps.users.tests.factories import UserFactory
from apps.profiles.models import Profile, TelegramData
from apps.units.tests.factories import DepartmentFactory
from faker import Factory
import factory

User = get_user_model()
faker = Factory.create()


@factory.django.mute_signals(post_save)
class ProfileFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    position = factory.LazyAttribute(lambda x: faker.job())
    department = factory.SubFactory(DepartmentFactory)
    avatar = factory.LazyAttribute(lambda x: faker.image_url())

    class Meta:
        model = Profile


class TelegramDataFactory(factory.django.DjangoModelFactory):
    profile = factory.SubFactory(ProfileFactory)
    telegram_user_id = factory.LazyAttribute(lambda x: faker.pyint())
    telegram_username = factory.LazyAttribute(lambda x: faker.user_name())
    telegram_first_name = factory.LazyAttribute(lambda x: faker.first_name())
    telegram_last_name = factory.LazyAttribute(lambda x: faker.last_name())
    is_verified = True

    class Meta:
        model = TelegramData


class ProfileWithTelegramFactory(ProfileFactory):
    @factory.post_generation
    def telegram(self, create, extracted, **kwargs):
        if create:
            TelegramDataFactory.create(profile=self, **kwargs)


class UserWithProfileFactory(UserFactory):
    @factory.post_generation
    def profile(self, create, extracted, **kwargs):
        if create:
            ProfileFactory.create(user=self)
