from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import Event, RecurringEvent


@receiver(pre_save, sender=Event)
def delete_old_image_on_update(sender, instance, **kwargs):
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
def delete_image_on_delete(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)


@receiver(post_delete, sender=RecurringEvent)
def set_recurring_flag_false(sender, instance, **kwargs):
    event = instance.event
    if event.is_recurring:
        event.is_recurring = False
        event.save(update_fields=['is_recurring'])
