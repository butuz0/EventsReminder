from django.db.models.signals import post_save
from apps.teams.models import Team, Invitation
from apps.users.tests.factories import UserFactory
from faker import Factory
import factory

faker = Factory.create()


class TeamFactory(factory.django.DjangoModelFactory):
    name = factory.LazyAttribute(lambda n: faker.company())
    description = factory.LazyAttribute(lambda n: faker.catch_phrase())
    created_by = factory.SubFactory(UserFactory)

    class Meta:
        model = Team

    @factory.post_generation
    def members(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for member in extracted:
                self.members.add(member)
        else:
            self.members.add(UserFactory())


@factory.django.mute_signals(post_save)
class InvitationFactory(factory.django.DjangoModelFactory):
    created_by = factory.SubFactory(UserFactory)
    team = factory.SubFactory(TeamFactory)
    sent_to = factory.SubFactory(UserFactory)
    status = factory.LazyAttribute(lambda x: Invitation.Status.PENDING)

    class Meta:
        model = Invitation
