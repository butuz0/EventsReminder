from django.urls import reverse
from .factories import TeamFactory, InvitationFactory
from apps.teams.models import Invitation
from apps.users.tests.factories import UserFactory
from faker import Faker
import pytest

fake = Faker()


@pytest.mark.django_db
def test_get_team_list(client, normal_user):
    TeamFactory.create_batch(3, created_by=normal_user)
    TeamFactory.create_batch(2, members=[normal_user])
    TeamFactory.create_batch(3)

    response = client.get(reverse('team-list'))

    assert response.status_code == 200
    assert len(response.data['results']) == 5


@pytest.mark.django_db
def test_get_team_list_unauthorized(client, normal_user):
    TeamFactory(created_by=normal_user)

    response = client.get(reverse('team-list'))

    assert response.status_code == 401
    assert response.data['detail'] == 'Authentication credentials were not provided.'


@pytest.mark.django_db
def test_get_team_detail(client, normal_user):
    team = TeamFactory(created_by=normal_user)

    response = client.get(reverse('team-detail', kwargs={'id': team.id}))

    assert response.status_code == 200
    assert response.data['id'] == str(team.id)


@pytest.mark.django_db
def test_remove_team_member(client, normal_user):
    user = UserFactory()
    team = TeamFactory(created_by=normal_user, members=[user])

    response = client.delete(
        reverse('team-remove-member',
                kwargs={
                    'team_id': team.id,
                    'user_id': user.id
                })
    )

    assert response.status_code == 204
    assert response.data['detail'] == 'Member deleted successfully.'


@pytest.mark.django_db
def test_remove_team_member_team_does_not_exist(client, normal_user):
    user = UserFactory()
    team_id = fake.uuid4()

    response = client.delete(
        reverse('team-remove-member',
                kwargs={
                    'team_id': team_id,
                    'user_id': user.id
                })
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_remove_team_member_user_does_not_exist(client, normal_user):
    user_id = fake.uuid4()
    team = TeamFactory(created_by=normal_user)

    response = client.delete(
        reverse('team-remove-member',
                kwargs={
                    'team_id': team.id,
                    'user_id': user_id
                })
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_remove_team_member_user_is_not_member(client, normal_user):
    user = UserFactory()
    team = TeamFactory(created_by=normal_user)

    response = client.delete(
        reverse('team-remove-member',
                kwargs={
                    'team_id': team.id,
                    'user_id': user.id
                })
    )

    assert response.status_code == 400
    assert response.data['detail'] == 'Користувач не є членом цієї команди.'


@pytest.mark.django_db
def test_team_leave(client, normal_user):
    team = TeamFactory(members=[normal_user])
    response = client.delete(
        reverse('team-leave',
                kwargs={'id': team.id})
    )

    assert response.status_code == 204
    assert response.data['detail'] == 'You have left the team.'


@pytest.mark.django_db
def test_team_leave_team_does_not_exist(client):
    team_id = fake.uuid4()
    response = client.delete(
        reverse('team-leave',
                kwargs={'id': team_id})
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_team_leave_team_user_is_creator(client, normal_user):
    team = TeamFactory(created_by=normal_user)
    response = client.delete(
        reverse('team-leave',
                kwargs={'id': team.id})
    )

    assert response.status_code == 403
    assert response.data['detail'] == 'Ви не можете покинути команду, лідером якої Ви є.'


@pytest.mark.django_db
def test_team_leave_team_not_member(client):
    team = TeamFactory()

    response = client.delete(
        reverse('team-leave',
                kwargs={'id': team.id})
    )

    assert response.status_code == 403
    assert response.data['detail'] == 'Ви не є членом цієї команди.'


@pytest.mark.django_db
def test_invitation_list(client, normal_user):
    InvitationFactory.create_batch(3, sent_to=normal_user)
    InvitationFactory.create_batch(2)

    response = client.get(reverse('invitation-list'))

    assert response.status_code == 200
    assert response.data['count'] == 3
    assert len(response.data['results']) == 3


@pytest.mark.django_db
def test_invitation_detail_sent_to_user(client, normal_user):
    invitation = InvitationFactory(sent_to=normal_user)

    response = client.get(
        reverse('invitation-detail',
                kwargs={'id': invitation.id})
    )

    assert response.status_code == 200
    assert response.data['id'] == str(invitation.id)
    assert response.data['sent_to']['id'] == str(normal_user.id)
    assert response.data['created_by']['id'] != str(normal_user.id)


@pytest.mark.django_db
def test_invitation_detail_created_by_user(client, normal_user):
    invitation = InvitationFactory(created_by=normal_user)

    response = client.get(
        reverse('invitation-detail',
                kwargs={'id': invitation.id})
    )

    assert response.status_code == 200
    assert response.data['id'] == str(invitation.id)
    assert response.data['sent_to']['id'] != str(normal_user.id)
    assert response.data['created_by']['id'] == str(normal_user.id)


@pytest.mark.django_db
def test_invitation_detail_other_user(client):
    invitation = InvitationFactory()

    response = client.get(
        reverse('invitation-detail',
                kwargs={'id': invitation.id})
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_invitation_respond(client, normal_user):
    invitation = InvitationFactory(sent_to=normal_user)

    response = client.patch(
        reverse('invitation-respond', kwargs={'id': invitation.id}),
        data={'status': Invitation.Status.ACCEPTED}
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_invitation_delete_user_created_by(client, normal_user):
    invitation = InvitationFactory(created_by=normal_user)

    response = client.delete(
        reverse('invitation-delete',
                kwargs={'id': invitation.id})
    )

    assert response.status_code == 204


@pytest.mark.django_db
def test_invitation_delete_user_sent_to(client, normal_user):
    invitation = InvitationFactory(sent_to=normal_user)

    response = client.delete(
        reverse('invitation-delete',
                kwargs={'id': invitation.id})
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_invitation_delete_other_user(client):
    invitation = InvitationFactory()

    response = client.delete(
        reverse('invitation-delete',
                kwargs={'id': invitation.id})
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_team_members_user_created_by(client, normal_user):
    users = UserFactory.create_batch(3)
    team = TeamFactory(
        created_by=normal_user,
        members=users
    )

    response = client.get(
        reverse('team-members',
                kwargs={'team_id': team.id})
    )

    assert response.status_code == 200
    assert response.data['count'] == 3
    assert len(response.data['results']) == 3
    assert set([member['id'] for member in response.data['results']]) == set([str(user.id) for user in users])


@pytest.mark.django_db
def test_team_members_team_does_not_exist(client):
    team_id = fake.uuid4()

    response = client.get(
        reverse('team-members',
                kwargs={'team_id': team_id})
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_team_members_user_member(client, normal_user):
    team = TeamFactory(members=[normal_user])

    response = client.get(
        reverse('team-members',
                kwargs={'team_id': team.id})
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_team_members_other_user(client):
    user = UserFactory()
    team = TeamFactory(members=[user])

    response = client.get(
        reverse('team-members',
                kwargs={'team_id': team.id})
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_team_invitations_user_created_by(client, normal_user):
    team = TeamFactory(created_by=normal_user)
    invitations = InvitationFactory.create_batch(3, team=team)
    InvitationFactory.create_batch(2)

    response = client.get(
        reverse('team-invitations',
                kwargs={'team_id': team.id})
    )

    assert response.status_code == 200
    assert response.data['count'] == 3
    assert len(response.data['results']) == 3
    assert set([inv['id'] for inv in response.data['results']]) == set([str(inv.id) for inv in invitations])


@pytest.mark.django_db
def test_team_invitations_team_does_not_exist(client):
    team_id = fake.uuid4()

    response = client.get(
        reverse('team-invitations',
                kwargs={'team_id': team_id})
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_team_invitations_user_member(client, normal_user):
    team = TeamFactory(members=[normal_user])
    InvitationFactory.create_batch(3, team=team)

    response = client.get(
        reverse('team-invitations',
                kwargs={'team_id': team.id})
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_team_invitations_other_user(client, normal_user):
    user = UserFactory()
    team = TeamFactory(members=[user])
    InvitationFactory.create_batch(3, team=team)

    response = client.get(
        reverse('team-invitations',
                kwargs={'team_id': team.id})
    )

    assert response.status_code == 403
