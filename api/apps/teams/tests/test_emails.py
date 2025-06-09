from .factories import InvitationFactory
from apps.teams.emails import send_team_invitation_email
from apps.profiles.tests.factories import UserWithProfileFactory
from config.settings.local import SITE_NAME, DEFAULT_FROM_EMAIL
from unittest.mock import patch
import pytest


@pytest.mark.django_db
@patch('apps.teams.emails.EmailMultiAlternatives')
@patch('apps.teams.emails.render_to_string')
def test_send_team_invitation_email(mock_render_to_string, mock_email_class, normal_user):
    invitation = InvitationFactory(sent_to=normal_user)

    mock_render_to_string.side_effect = ['HTML email', 'Text email']
    mock_email_instance = mock_email_class.return_value

    send_team_invitation_email(normal_user, invitation)

    assert mock_render_to_string.call_count == 2

    mock_render_to_string.assert_any_call('invitations/team_invitation_email.html', {
        'user': normal_user,
        'invitation': invitation,
        'site_name': SITE_NAME
    })
    mock_render_to_string.assert_any_call('invitations/team_invitation_email.txt', {
        'user': normal_user,
        'invitation': invitation,
        'site_name': SITE_NAME
    })

    mock_email_class.assert_called_once_with(
        f'Invitation to join team "{invitation.team.name}"',
        'Text email',
        DEFAULT_FROM_EMAIL,
        [normal_user.email],
    )

    mock_email_instance.attach_alternative.assert_called_once_with('HTML email', 'text/html')
    mock_email_instance.send.assert_called_once()
