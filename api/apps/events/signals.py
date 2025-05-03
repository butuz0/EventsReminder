from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import Event


@receiver(pre_save, sender=Event)
def delete_old_image_on_update(sender, instance, **kwargs):
    if not instance.id:
        return

    old_image = Event.objects.only('image').get(id=instance.id).image
    new_image = instance.image

    if old_image and old_image != new_image:
        old_image.delete(save=False)


@receiver(post_delete, sender=Event)
def delete_image_on_delete(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)
