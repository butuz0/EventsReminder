from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from apps.common.renderers import JSONRenderer
from apps.events.models import Event
from apps.events.serializers import EventDetailSerializer
from .permissions import IsOwner, IsOwnerOrMember
from .models import Team, Invitation
from .serializers import (
    TeamCreateSerializer,
    TeamUpdateSerializer,
    TeamDetailSerializer,
    InvitationCreateSerializer,
    InvitationDetailSerializer,
    InvitationRespondSerializer
)
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from djoser.serializers import UserSerializer

User = get_user_model()


class TeamListAPIView(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamDetailSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    object_label = 'teams'

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(Q(created_by=user) | Q(members=user)).distinct()


class TeamCreateAPIView(generics.CreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamCreateSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    object_label = 'team'


class TeamUpdateAPIView(generics.UpdateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    renderer_classes = [JSONRenderer]
    object_label = 'team'
    lookup_field = 'id'


class TeamDetailAPIView(generics.RetrieveAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamDetailSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrMember]
    renderer_classes = [JSONRenderer]
    object_label = 'team'
    lookup_field = 'id'


class TeamDeleteAPIView(generics.DestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamDetailSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = 'id'


class RemoveTeamMemberView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, team_id, user_id):
        team = get_object_or_404(Team, id=team_id, created_by=request.user)
        user = get_object_or_404(User, id=user_id)

        if user not in team.members.all():
            return Response({'detail': 'User is not a member of this team.'},
                            status=status.HTTP_400_BAD_REQUEST)

        team.members.remove(user)
        return Response({'detail': 'Member deleted successfully.'},
                        status=status.HTTP_204_NO_CONTENT)


class TeamLeaveAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        user = request.user
        team = get_object_or_404(Team, id=id)

        if team.created_by == user:
            return Response({'detail': 'You cannot leave a team that you have created.'},
                            status=status.HTTP_403_FORBIDDEN)

        if not team.members.filter(id=user.id).exists():
            raise PermissionDenied('You are not a member of this team.')

        team.members.remove(user)
        return Response({'detail': 'You have left the team.'},
                        status=status.HTTP_204_NO_CONTENT)


class InvitationListCreateAPIView(generics.ListCreateAPIView):
    queryset = Invitation.objects.all()
    serializer_class = InvitationCreateSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    object_label = 'invitations'


class InvitationListAPIView(generics.ListCreateAPIView):
    queryset = Invitation.objects.all()
    serializer_class = InvitationDetailSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    object_label = 'invitations'

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(sent_to=user)


class InvitationDetailAPIView(generics.RetrieveAPIView):
    queryset = Invitation.objects.all()
    serializer_class = InvitationDetailSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    object_label = 'invitations'
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(Q(created_by=user) | Q(sent_to=user))


class InvitationRespondAPIView(generics.UpdateAPIView):
    queryset = Invitation.objects.all()
    serializer_class = InvitationRespondSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(sent_to=user)


class InvitationDeleteAPIView(generics.DestroyAPIView):
    queryset = Invitation.objects.all()
    serializer_class = InvitationDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(created_by=user)


class TeamMembersListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        team = get_object_or_404(Team, id=self.kwargs['team_id'],
                                 created_by=self.request.user)
        return team.members.all()


class TeamEventsListAPIView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventDetailSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    object_label = 'events'

    def get_queryset(self):
        team_id = self.kwargs['team_id']
        team = get_object_or_404(Team, id=team_id)

        permission = IsOwnerOrMember()
        if not permission.has_object_permission(self.request, self, team):
            raise PermissionDenied(detail=permission.message)

        return Event.objects.filter(team=team)


class TeamInvitationsListAPIView(generics.ListAPIView):
    queryset = Invitation.objects.all()
    serializer_class = InvitationDetailSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]
    object_label = 'invitations'

    def get_queryset(self):
        team_id = self.kwargs['team_id']
        team = get_object_or_404(Team, id=team_id)

        permission = IsOwner()
        if not permission.has_object_permission(self.request, self, team):
            raise PermissionDenied(detail=permission.message)

        return Invitation.objects.filter(team=team)
