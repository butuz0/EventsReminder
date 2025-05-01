from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from config.settings.local import SITE_NAME, DEFAULT_FROM_EMAIL
from .models import Invitation


def send_team_invitation_email(user, invitation: Invitation) -> None:
    subject = f'Invitation to join team "{invitation.team.name}"'
    from_email = DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    context = {
        'user': user,
        'invitation': invitation,
        'site_name': SITE_NAME
    }

    html_email = render_to_string('invitations/team_invitation_email.html', context)
    text_email = render_to_string('invitations/team_invitation_email.txt', context)

    email = EmailMultiAlternatives(subject, text_email, from_email, recipient_list)
    email.attach_alternative(html_email, 'text/html')
    email.send()
