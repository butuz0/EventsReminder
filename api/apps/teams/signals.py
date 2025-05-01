from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Invitation
from .tasks import send_team_invitation_email_task


@receiver(post_save, sender=Invitation)
def create_celery_invitation_task(sender, instance: Invitation, created: bool, **kwargs):
    if created:
        send_team_invitation_email_task.delay(instance.id)
