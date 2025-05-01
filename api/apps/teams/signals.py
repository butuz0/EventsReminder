from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Invitation
from .emails import send_team_invitation_email


@receiver(post_save, sender=Invitation)
def create_celery_invitation_task(sender, instance: Invitation, created: bool, **kwargs):
    if created:
        user = instance.sent_to
        send_team_invitation_email(user, instance)
