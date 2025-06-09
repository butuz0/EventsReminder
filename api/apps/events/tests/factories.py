from django.db.models.signals import pre_save, post_delete, post_save
from django.utils.timezone import make_aware
from apps.events.models import Event, RecurringEvent
from apps.teams.tests.factories import TeamFactory
from apps.users.tests.factories import UserFactory
from faker import Factory
from datetime import datetime
import factory

faker = Factory.create()


@factory.django.mute_signals(pre_save)
@factory.django.mute_signals(post_delete)
class EventFactory(factory.django.DjangoModelFactory):
    created_by = factory.SubFactory(UserFactory)
    title = factory.LazyAttribute(lambda x: faker.word())
    priority = Event.Priority.MEDIUM
    start_datetime = factory.LazyFunction(lambda: make_aware(datetime.now()))

    team = factory.SubFactory(TeamFactory)
    description = factory.LazyAttribute(lambda x: faker.text())
    location = factory.LazyAttribute(lambda x: faker.city())
    link = factory.LazyAttribute(lambda x: faker.url())
    image = factory.LazyAttribute(lambda x: faker.image_url())
    is_recurring = False

    class Meta:
        model = Event

    @factory.post_generation
    def assigned_to(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for member in extracted:
                self.assigned_to.add(member)
        else:
            self.assigned_to.add(UserFactory())

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for tag in extracted:
                self.tags.add(tag)
        else:
            self.tags.add(faker.word(), faker.word())


@factory.django.mute_signals(post_save)
@factory.django.mute_signals(post_delete)
class RecurringEventFactory(factory.django.DjangoModelFactory):
    event = factory.SubFactory(EventFactory, is_recurring=True)
    recurrence_rule = RecurringEvent.RecurrenceRule.WEEKLY
    recurrence_end_datetime = factory.LazyFunction(lambda: make_aware(datetime.now()))
    celery_task_id = factory.LazyAttribute(lambda x: faker.uuid4())

    class Meta:
        model = RecurringEvent
