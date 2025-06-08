from apps.registration_cards.models import RegistrationCard
from apps.users.tests.factories import UserFactory
from faker import Factory
import factory

faker = Factory.create()


class RegistrationCardFactory(factory.django.DjangoModelFactory):
    created_by = factory.SubFactory(UserFactory)
    organization_name = factory.LazyAttribute(lambda x: faker.company())
    edrpou_code = factory.LazyAttribute(lambda x: faker.numerify(text='########'))
    region = factory.LazyAttribute(lambda x: faker.state())
    city = factory.LazyAttribute(lambda x: faker.city())
    full_name = factory.LazyAttribute(lambda x: faker.name())
    id_number = factory.LazyAttribute(lambda x: faker.numerify(text='##########'))
    keyword_phrase = factory.LazyAttribute(lambda x: faker.word())
    voice_phrase = factory.LazyAttribute(lambda x: faker.word())
    email = factory.LazyAttribute(lambda x: faker.email())
    phone_number = factory.LazyAttribute(lambda x: faker.phone_number()[:20])
    electronic_seal_name = factory.LazyAttribute(lambda x: faker.word())
    electronic_seal_keyword_phrase = factory.LazyAttribute(lambda x: faker.word())

    class Meta:
        model = RegistrationCard
