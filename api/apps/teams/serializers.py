from django.contrib.auth import get_user_model
from .models import Team, Invitation
from apps.users.serializers import CustomUserSerializer
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
        if not value:
            return []
        if self.context['request'].user.id in value:
            raise serializers.ValidationError('Ви не можете додати себе у команду, оскільки Ви її лідер.')

        user_ids = set(value)
        if len(user_ids) != len(value):
            raise serializers.ValidationError('Надано дублюючі ID користувачів.')

        existing_ids = set(User.objects.filter(id__in=user_ids).values_list('id', flat=True))
        missing_ids = user_ids - existing_ids
        if missing_ids:
            raise serializers.ValidationError(f'Не знайдено користувачів із наступними ID: {list(missing_ids)}')

        return value

    def create(self, validated_data: dict) -> Team:
        user = self.context['request'].user
        members_ids = validated_data.pop('members_ids', [])

        team = Team.objects.create(created_by=user, **validated_data)

        # Create invitation for each member
        members = User.objects.filter(id__in=members_ids)
        for member in members:
            Invitation.objects.create(created_by=user, team=team, sent_to=member)

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
        fields = ['id', 'name', 'description', 'created_by',
                  'members', 'created_at', 'updated_at']
        read_only_fields = fields


class InvitationCreateSerializer(serializers.ModelSerializer):
    team = serializers.UUIDField()
    sent_to = serializers.UUIDField()

    class Meta:
        model = Invitation
        fields = ['id', 'team', 'created_by', 'sent_to',
                  'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_by']

    def validate_team(self, value: str) -> Team:
        try:
            team = Team.objects.get(id=value)
        except Team.DoesNotExist:
            raise serializers.ValidationError('Команди не знайдено.')
        return team

    def validate_sent_to(self, value: str):
        try:
            user = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('Користувача не знайдено.')
        return user

    def validate(self, attrs: dict) -> dict:
        user = self.context['request'].user
        team = attrs.get('team')
        sent_to = attrs.get('sent_to')

        if user != team.created_by:
            raise serializers.ValidationError('Лише лідер команди може створювати запрошення.')
        if sent_to == user:
            raise serializers.ValidationError('Ви не можете запросити себе.')
        if sent_to in team.members.all():
            raise serializers.ValidationError('Користувач вже є членом команди.')
        if Invitation.objects.filter(team=team, sent_to=sent_to, status=Invitation.Status.PENDING).exists():
            raise serializers.ValidationError('Запрошення вже було створено раніше.')
        return attrs

    def create(self, validated_data: dict) -> Invitation:
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class InvitationDetailSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='team.name')
    team_description = serializers.CharField(source='team.description')
    sent_to = CustomUserSerializer()
    created_by = CustomUserSerializer()

    class Meta:
        model = Invitation
        fields = ['id', 'sent_to', 'created_by', 'team_name',
                  'team_description', 'status',
                  'created_at', 'updated_at']


class InvitationRespondSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=Invitation.Status.choices, required=True)

    class Meta:
        model = Invitation
        fields = ['status']

    def validate(self, attrs: dict) -> dict:
        instance = self.instance

        if instance.status != Invitation.Status.PENDING:
            raise serializers.ValidationError('На запрошення вже було надано відповідь.')

        return attrs

    def update(self, instance: Invitation, validated_data: dict) -> Invitation:
        instance.status = validated_data['status']
        instance.save()

        if instance.status == Invitation.Status.ACCEPTED:
            instance.team.members.add(instance.sent_to)

        return instance
