from .factories import TeamFactory, InvitationFactory
import pytest


@pytest.mark.django_db
def test_team_str():
    team = TeamFactory()
    assert str(team) == f'{team.name} - {team.created_by}'


@pytest.mark.django_db
def test_invitation_str(normal_user):
    team = TeamFactory()
    invitation = InvitationFactory(
        team=team,
        sent_to=normal_user
    )
    assert str(invitation) == f'{invitation.sent_to} - {invitation.team}'
