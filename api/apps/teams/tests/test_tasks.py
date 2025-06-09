from apps.teams.models import Invitation
from apps.teams.tasks import send_team_invitation_email_task
from apps.teams.tests.factories import InvitationFactory
from unittest.mock import patch
from faker import Faker
import pytest

fake = Faker()


@pytest.mark.django_db
@patch('apps.teams.tasks.send_team_invitation_email')
def test_send_team_invitation_email_task_success(mock_send_email):
    invitation = InvitationFactory()

    send_team_invitation_email_task(str(invitation.id))

    mock_send_email.assert_called_once_with(invitation.sent_to, invitation)


@pytest.mark.django_db
@patch('apps.teams.tasks.send_team_invitation_email')
def test_send_team_invitation_email_task_invitation_does_not_exist(mock_send_email):
    invitation_id = fake.uuid4()

    send_team_invitation_email_task(str(invitation_id))

    mock_send_email.assert_not_called()
