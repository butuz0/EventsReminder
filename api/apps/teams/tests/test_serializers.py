from .factories import TeamFactory, InvitationFactory
from apps.teams.models import Invitation
from apps.teams.serializers import (
    TeamCreateSerializer,
    InvitationCreateSerializer,
    InvitationRespondSerializer
)
from apps.users.tests.factories import UserFactory
from rest_framework.test import APIRequestFactory
from faker import Faker
import pytest

fake = Faker()


def get_request(user):
    factory = APIRequestFactory()
    request = factory.post('/fake-url')
    request.user = user
    return request


@pytest.mark.django_db
def test_team_create_serializer_success(normal_user):
    members = UserFactory.create_batch(3)
    members_ids = [user.id for user in members]

    data = {
        'name': 'Test team',
        'description': 'Test description',
        'members_ids': members_ids
    }
    context = {'request': get_request(normal_user)}

    serializer = TeamCreateSerializer(data=data, context=context)
    assert serializer.is_valid()

    team = serializer.save()
    assert team.name == 'Test team'
    assert team.description == 'Test description'
    assert team.created_by == normal_user
    assert team.members.count() == 0
    assert Invitation.objects.filter(team=team, created_by=normal_user).count() == 3

    expected_ids = set(members_ids)
    actual_ids = set(Invitation.objects.filter(team=team).values_list('sent_to__id', flat=True))
    assert actual_ids == expected_ids


@pytest.mark.django_db
def test_team_create_serializer_no_members(normal_user):
    data = {
        'name': 'Test team',
        'members_ids': []
    }
    context = {'request': get_request(normal_user)}
    serializer = TeamCreateSerializer(data=data, context=context)
    assert serializer.is_valid()

    team = serializer.save()
    assert team.members.count() == 0
    assert Invitation.objects.filter(team=team, created_by=normal_user).count() == 0


def test_team_create_serializer_creator_in_members(normal_user):
    members = UserFactory.create_batch(3)
    members_ids = [user.id for user in members] + [normal_user.id]
    data = {
        'name': 'Test team',
        'members_ids': members_ids

    }
    context = {'request': get_request(normal_user)}
    serializer = TeamCreateSerializer(data=data, context=context)
    assert not serializer.is_valid()

    assert 'members_ids' in serializer.errors
    assert serializer.errors['members_ids'][0] == 'Ви не можете додати себе у команду, оскільки Ви її лідер.'


def test_team_create_serializer_duplicate_members(normal_user):
    members = UserFactory.create_batch(3)
    members_ids = [user.id for user in members] + [members[0].id]
    data = {
        'name': 'Test team',
        'members_ids': members_ids

    }
    context = {'request': get_request(normal_user)}
    serializer = TeamCreateSerializer(data=data, context=context)
    assert not serializer.is_valid()

    assert 'members_ids' in serializer.errors
    assert serializer.errors['members_ids'][0] == 'Надано дублюючі ID користувачів.'


def test_team_create_serializer_member_does_not_exist(normal_user):
    members = UserFactory.create_batch(3)
    members_ids = [user.id for user in members] + [fake.uuid4()]
    data = {
        'name': 'Test team',
        'members_ids': members_ids
    }
    context = {'request': get_request(normal_user)}
    serializer = TeamCreateSerializer(data=data, context=context)
    assert not serializer.is_valid()

    assert 'members_ids' in serializer.errors
    assert 'Не знайдено користувачів із наступними ID' in serializer.errors['members_ids'][0]


@pytest.mark.django_db
def test_invitation_create_serializer_success(normal_user):
    team = TeamFactory(created_by=normal_user)
    sent_to = UserFactory()
    data = {
        'team': team.id,
        'sent_to': sent_to.id,
    }
    context = {'request': get_request(normal_user)}
    serializer = InvitationCreateSerializer(data=data, context=context)
    assert serializer.is_valid()

    invitation = serializer.save()
    assert invitation.team == team
    assert invitation.created_by == normal_user
    assert invitation.sent_to == sent_to


def test_invitation_create_does_not_exist(normal_user):
    data = {
        'team': fake.uuid4(),
        'sent_to': fake.uuid4(),
    }
    context = {'request': get_request(normal_user)}
    serializer = InvitationCreateSerializer(data=data, context=context)
    assert not serializer.is_valid()

    assert 'team' in serializer.errors
    assert 'sent_to' in serializer.errors
    assert serializer.errors['team'][0] == 'Команди не знайдено.'
    assert serializer.errors['sent_to'][0] == 'Користувача не знайдено.'


def test_invitation_create_created_by_other_user(normal_user):
    team_owner = UserFactory()
    sent_to = UserFactory()
    team = TeamFactory(created_by=team_owner)
    data = {
        'team': team.id,
        'sent_to': sent_to.id,
    }
    context = {'request': get_request(normal_user)}
    serializer = InvitationCreateSerializer(data=data, context=context)
    assert not serializer.is_valid()

    assert serializer.errors['non_field_errors'][0] == 'Лише лідер команди може створювати запрошення.'


def test_validate_invite_self(normal_user):
    team = TeamFactory(created_by=normal_user)
    data = {
        'team': team.id,
        'sent_to': normal_user.id
    }
    context = {'request': get_request(normal_user)}
    serializer = InvitationCreateSerializer(data=data, context=context)
    assert not serializer.is_valid()

    assert serializer.errors['non_field_errors'][0] == 'Ви не можете запросити себе.'


def test_validate_user_already_member(normal_user):
    member = UserFactory()
    team = TeamFactory(created_by=normal_user, members=[member])
    data = {
        'team': team.id,
        'sent_to': member.id
    }
    context = {'request': get_request(normal_user)}

    serializer = InvitationCreateSerializer(data=data, context=context)
    assert not serializer.is_valid()

    assert serializer.errors['non_field_errors'][0] == 'Користувач вже є членом команди.'


@pytest.mark.django_db
def test_validate_invitation_already_pending(normal_user):
    sent_to = UserFactory()
    team = TeamFactory(created_by=normal_user)
    InvitationFactory(
        team=team,
        created_by=normal_user,
        sent_to=sent_to,
    )

    data = {
        'team': team.id,
        'sent_to': sent_to.id
    }
    context = {'request': get_request(normal_user)}
    serializer = InvitationCreateSerializer(data=data, context=context)
    assert not serializer.is_valid()

    assert serializer.errors['non_field_errors'][0] == 'Запрошення вже було створено раніше.'


@pytest.mark.django_db
def test_invitation_respond_accept(normal_user):
    invitation = InvitationFactory(sent_to=normal_user)

    data = {'status': Invitation.Status.ACCEPTED}
    serializer = InvitationRespondSerializer(instance=invitation, data=data)
    assert serializer.is_valid()

    instance = serializer.save()
    assert instance.status == Invitation.Status.ACCEPTED
    assert normal_user in list(invitation.team.members.all())


@pytest.mark.django_db
def test_invitation_respond_reject(normal_user):
    invitation = InvitationFactory(sent_to=normal_user)

    data = {'status': Invitation.Status.REJECTED}
    serializer = InvitationRespondSerializer(instance=invitation, data=data)
    assert serializer.is_valid()

    instance = serializer.save()
    assert instance.status == Invitation.Status.REJECTED
    assert normal_user not in list(invitation.team.members.all())


def test_invitation_respond_missing_status(normal_user):
    invitation = InvitationFactory(sent_to=normal_user)

    serializer = InvitationRespondSerializer(instance=invitation, data={})
    assert not serializer.is_valid()

    assert 'status' in serializer.errors
    assert serializer.errors['status'][0] == 'This field is required.'


def test_invitation_respond_already_responded(normal_user):
    invitation = InvitationFactory(
        sent_to=normal_user,
        status=Invitation.Status.ACCEPTED
    )

    data = {'status': Invitation.Status.REJECTED}
    serializer = InvitationRespondSerializer(instance=invitation, data=data)
    assert not serializer.is_valid()

    assert serializer.errors['non_field_errors'][0] == 'На запрошення вже було надано відповідь.'
