from django.utils.timezone import now
from django.contrib.auth import get_user_model
from .models import Event, RecurringEvent
from .recurring import reschedule_recurring_event
from apps.teams.models import Team
from apps.users.serializers import CustomUserSerializer
from rest_framework import serializers
from taggit.serializers import TagListSerializerField, TaggitSerializer
from djoser.serializers import UserSerializer
from datetime import datetime
from celery.result import AsyncResult

User = get_user_model()


class RecurringEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringEvent
        fields = [
            'id', 'recurrence_rule', 'recurrence_end_datetime',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_recurrence_end_datetime(self, value: datetime) -> datetime:
        if value and value < now():
            raise serializers.ValidationError('End date must be in the future.')
        return value

    def validate(self, data: dict) -> dict:
        if self.instance:
            event = self.instance.event  # if object already exists
        else:
            event = self.context.get('event')  # if object is being created

        if event and data.get('recurrence_end_datetime') and data['recurrence_end_datetime'] < event.start_datetime:
            raise serializers.ValidationError('End date must be after event start date.')
        return data

    def create(self, validated_data: dict) -> RecurringEvent:
        event = validated_data.pop('event', None) or self.context.get('event')
        if not event:
            raise serializers.ValidationError('Event must be provided.')

        recurring = RecurringEvent.objects.create(event=event, **validated_data)
        reschedule_recurring_event(recurring)
        return recurring

    def update(self, instance: RecurringEvent, validated_data: dict) -> RecurringEvent:
        recurring = super().update(instance, validated_data)
        reschedule_recurring_event(instance)
        return recurring


class BaseEventSerializer(TaggitSerializer, serializers.ModelSerializer):
    assigned_to_ids = serializers.ListField(child=serializers.UUIDField(), write_only=True, required=False)
    assigned_to = CustomUserSerializer(many=True, read_only=True)
    tags = TagListSerializerField(required=False)

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'start_datetime',
                  'location', 'link', 'priority', 'image',
                  'tags', 'assigned_to_ids', 'assigned_to',
                  'is_recurring']

    def validate_start_datetime(self, value: datetime) -> datetime:
        if value < now():
            raise serializers.ValidationError('Event start time cannot be in the past.')
        return value

    def validate_assigned_to_ids(self, value: list[str]) -> list[str]:
        user = self.context['request'].user

        if user.id in value:
            raise serializers.ValidationError('You cannot assign the event to yourself.')

        # Check if any user IDs are duplicates
        user_ids = set(value)
        if len(user_ids) != len(value):
            raise serializers.ValidationError('Duplicate user IDs are not allowed.')

        # Check if all users exist
        existing_ids = set(
            User.objects
            .filter(id__in=user_ids)
            .values_list('id', flat=True)
        )
        missing_ids = user_ids - existing_ids
        if missing_ids:
            raise serializers.ValidationError(f'Users with the following IDs do not exist: {list(missing_ids)}')

        return value


class EventCreateSerializer(BaseEventSerializer):
    team = serializers.UUIDField(required=False)

    class Meta(BaseEventSerializer.Meta):
        fields = BaseEventSerializer.Meta.fields + ['team']

    def validate_team(self, value: str) -> str:
        try:
            team = Team.objects.get(id=value)
        except Team.DoesNotExist:
            raise serializers.ValidationError('Team does not exist.')

        if self.context['request'].user != team.created_by:
            raise serializers.ValidationError('Only team owner can create events.')

        return value

    def validate(self, attrs: dict) -> dict:
        team_id = attrs.get('team')
        if not team_id:
            return attrs

        # Check if all users are members of the provided team
        team = Team.objects.get(id=team_id)

        assigned_to_ids = set(attrs.get('assigned_to_ids'))
        team_member_ids = set(team.members.values_list('id', flat=True))

        if not assigned_to_ids.issubset(team_member_ids):
            invalid_ids = assigned_to_ids - team_member_ids
            raise serializers.ValidationError(
                f'The following users are not members of the selected team: {list(invalid_ids)}'
            )
        return attrs

    def create(self, validated_data: dict) -> Event:
        tags = validated_data.pop('tags', [])
        assigned_to = validated_data.pop('assigned_to_ids', [])
        team_id = validated_data.pop('team', None)
        team = Team.objects.get(id=team_id) if team_id else None
        user = self.context['request'].user

        event = Event.objects.create(created_by=user, team=team, **validated_data)
        event.assigned_to.set(User.objects.filter(id__in=assigned_to))
        event.tags.set(tags)

        return event


class EventUpdateSerializer(BaseEventSerializer):
    class Meta(BaseEventSerializer.Meta):
        fields = BaseEventSerializer.Meta.fields

    def update(self, instance: Event, validated_data: dict) -> Event:
        tags = validated_data.pop('tags', None)
        assigned_to = validated_data.pop('assigned_to_ids', None)
        old_datetime = instance.start_datetime
        new_datetime = validated_data.get('start_datetime', old_datetime)

        # Delete RecurringEvent instance if is_recurring is set from True to False
        if not validated_data.get('is_recurring', True) and hasattr(instance, 'recurring_event'):
            instance.recurring_event.delete()

        # Update standard model fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if instance.is_recurring and hasattr(instance, 'recurring_event') and old_datetime != new_datetime:
            reschedule_recurring_event(instance.recurring_event)

        # Update tags field
        if tags is not None:
            instance.tags.set(tags)

        # Update assigned_to field
        if assigned_to is not None:
            assigned_to_users = User.objects.filter(id__in=assigned_to)
            instance.assigned_to.set(assigned_to_users)

        return instance


class EventDetailSerializer(serializers.ModelSerializer):
    tags = TagListSerializerField()
    created_by = UserSerializer(read_only=True)
    assigned_to = CustomUserSerializer(many=True, read_only=True)
    recurring_event = RecurringEventSerializer(read_only=True)
    image_url = serializers.SerializerMethodField()
    team = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'created_by', 'title', 'description',
                  'start_datetime', 'location', 'link',
                  'priority', 'image_url', 'tags', 'assigned_to',
                  'is_recurring', 'recurring_event', 'team', 'created_at']

    def get_team(self, obj: Event) -> dict | None:
        if obj.team:
            return {
                'id': str(obj.team.id),
                'name': obj.team.name
            }
        return None

    def get_image_url(self, obj: Event) -> str | None:
        request = self.context.get('request')
        if obj.image and request:
            url = request.build_absolute_uri(obj.image.url)
            if url.startswith('http://localhost/'):
                return url.replace('http://localhost/', 'http://localhost:8080/')
            return url
        return None
