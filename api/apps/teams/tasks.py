from django.contrib.auth import get_user_model
from .models import Team, Invitation
from .emails import send_team_invitation_email
from celery import shared_task

User = get_user_model()


@shared_task
def send_team_invitation_email_task(invitation_id: str) -> None:
    try:
        invitation = Invitation.objects.select_related('sent_to', 'team', 'created_by').get(id=invitation_id)
        user = invitation.sent_to
        send_team_invitation_email(user, invitation)
    except Invitation.DoesNotExist:
        pass
