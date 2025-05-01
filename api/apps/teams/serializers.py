from django.utils.timezone import now
from django.contrib.auth import get_user_model
from apps.users.serializers import CustomUserSerializer
from .models import Team, Invitation
from rest_framework import serializers

User = get_user_model()


class TeamCreateSerializer(serializers.ModelSerializer):
    members_ids = serializers.ListField(child=serializers.UUIDField(), write_only=True, required=False)
    
    class Meta:
        model = Team
        fields = [
            'id', 'created_by', 'name', 'description', 'members_ids', 
            'members', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'members', 'created_at', 'updated_at']
        
    def validate_members_ids(self, value: list[str]) -> list[str]:
        if self.context['request'].user.id in value:
            raise serializers.ValidationError('You cannot add yourself to the team since you are the creator of it.')
        return value

    def create(self, validated_data: dict) -> Team:
        user = self.context['request'].user
        members_ids = validated_data.pop('members_ids', [])
        if len(set(members_ids)) != len(members_ids):
            raise serializers.ValidationError('Duplicate user IDs are not allowed.')

        team = Team.objects.create(created_by=user, **validated_data)

        # Create invitation for each member
        for member_id in members_ids:
            sent_to = User.objects.get(id=member_id)
            Invitation.objects.create(
                created_by=user,
                team=team,
                sent_to=sent_to
            )
        
        return team


class TeamUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'description']


class TeamDetailSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    members = CustomUserSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'created_by', 'members', 'created_at', 'updated_at']
        read_only_fields = fields


class InvitationCreateSerializer(serializers.ModelSerializer):
    team = serializers.UUIDField()
    sent_to = serializers.UUIDField()
    
    class Meta:
        model = Invitation
        fields = ['id', 'team', 'created_by', 'sent_to']
        read_only_fields = ['id', 'created_by']
    
    def validate_team(self, value: str) -> Team:
        try:
            team = Team.objects.get(id=value)
        except Team.DoesNotExist:
            raise serializers.ValidationError('Team does not exist.')
        return team
    
    def validate_sent_to(self, value: str):
        try:
            user = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('User does not exist.')
        return user
    
    def validate(self, attrs):
        user = self.context['request'].user
        team = attrs.get('team')
        sent_to = attrs.get('sent_to')

        if user != team.created_by:
            raise serializers.ValidationError('Only team owner can send invitations.')
        if sent_to == user:
            raise serializers.ValidationError('You cannot invite yourself.')
        if sent_to in team.members.all():
            raise serializers.ValidationError('User is already a member of the team.')
        if Invitation.objects.filter(team=team, sent_to=sent_to, status=Invitation.Status.PENDING).exists():
            raise serializers.ValidationError('Invitation already pending.')
        return attrs

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class InvitationDetailSerializer(serializers.ModelSerializer):
    team = TeamDetailSerializer()
    sent_to = CustomUserSerializer()
    created_by = CustomUserSerializer()

    class Meta:
        model = Invitation
        fields = ['id', 'team', 'sent_to', 'created_by', 'status', 'created_at', 'updated_at']


class InvitationRespondSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['status']

    def update(self, instance: Invitation, validated_data: dict) -> Invitation:
        if instance.status != Invitation.Status.PENDING:
            raise serializers.ValidationError('Invitation already responded.')

        instance.status = validated_data.pop('status', None)
        
        if not instance.status:
            raise serializers.ValidationError('Status is required.')
        
        instance.save()

        if instance.status == Invitation.Status.ACCEPTED:
            instance.team.members.add(instance.sent_to)

        return instance
