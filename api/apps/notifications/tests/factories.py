from django.db.models.signals import post_delete, post_save
from django.utils.timezone import make_aware
from apps.notifications.models import Notification
from apps.events.tests.factories import EventFactory
from apps.users.tests.factories import UserFactory
from datetime import datetime, timedelta
from faker import Factory
import factory

faker = Factory.create()


@factory.django.mute_signals(post_save, post_delete)
class NotificationFactory(factory.django.DjangoModelFactory):
    event = factory.SubFactory(EventFactory)
    created_by = factory.SubFactory(UserFactory)
    notification_method = Notification.NotificationMethod.EMAIL
    notification_datetime = factory.LazyFunction(lambda: make_aware(datetime.now() + timedelta(days=1)))
    celery_task_id = factory.LazyAttribute(lambda x: faker.uuid4())
    is_sent = False

    class Meta:
        model = Notification
