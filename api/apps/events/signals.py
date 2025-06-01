from django.db.models.signals import pre_save, post_delete, post_save
from django.dispatch import receiver
from .models import Event, RecurringEvent
from .recurring import reschedule_recurring_event
from celery.result import AsyncResult


@receiver(pre_save, sender=Event)
def delete_old_image_on_update(sender, instance: Event, **kwargs):
    if not instance.id:
        return

    try:
        old_image = Event.objects.only('image').get(pk=instance.pk).image
    except Event.DoesNotExist:
        return

    new_image = instance.image

    if old_image and old_image != new_image:
        old_image.delete(save=False)


@receiver(post_delete, sender=Event)
def delete_image_on_delete(sender, instance: Event, **kwargs):
    if instance.image:
        instance.image.delete(save=False)


@receiver(post_save, sender=RecurringEvent)
def create_calculate_next_occurrence_task(sender, instance: RecurringEvent, created: bool, **kwargs):
    if not instance.event.is_recurring:
        return

    reschedule_recurring_event(instance)


@receiver(post_delete, sender=RecurringEvent)
def set_recurring_flag_false(sender, instance: RecurringEvent, **kwargs):
    event = instance.event
    if event.is_recurring:
        event.is_recurring = False
        event.save(update_fields=['is_recurring'])


@receiver(post_delete, sender=RecurringEvent)
def delete_event_rescheduling_celery_task(sender, instance: RecurringEvent, **kwargs):
    if instance.celery_task_id:
        AsyncResult(instance.celery_task_id).revoke(terminate=True)
