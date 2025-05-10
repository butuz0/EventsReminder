from django.utils.timezone import now
from django.contrib.auth import get_user_model
from .models import Event, RecurringEvent
from rest_framework import serializers
from taggit.serializers import TagListSerializerField, TaggitSerializer
from djoser.serializers import UserSerializer
from datetime import datetime

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
            raise serializers.ValidationError("End date must be in the future.")
        return value

    def validate(self, data: dict) -> dict:
        if self.instance:
            event = self.instance.event  # if object already exists
        else:
            event = self.context.get('event')  # if object is being created

        if event and data.get('recurrence_end_datetime') and data['recurrence_end_datetime'] < event.start_datetime:
            raise serializers.ValidationError('End date must be after event start date.')
        return data


class EventSerializer(TaggitSerializer, serializers.ModelSerializer):
    assigned_to_ids = serializers.ListField(child=serializers.UUIDField(), write_only=True, required=False)
    assigned_to = UserSerializer(many=True, read_only=True)
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

        if user in value:
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

        # Check if all users are members of the creator's teams
        team_members = set(
            User.objects
            .filter(teams__created_by=user, id__in=user_ids)
            .values_list('id', flat=True)
        )
        non_team_members = user_ids - team_members
        if non_team_members:
            raise serializers.ValidationError(
                f'You can only assign events to users who are members '
                f'of your team. Invalid IDs: {list(non_team_members)}'
            )

        return value

    def create(self, validated_data: dict) -> Event:
        tags = validated_data.pop('tags', [])
        assigned_to = validated_data.pop('assigned_to_ids', [])
        user = self.context['request'].user

        event = Event.objects.create(created_by=user, **validated_data)
        event.tags.set(tags)

        assigned_to_users = User.objects.filter(id__in=assigned_to)
        event.assigned_to.set(assigned_to_users)

        return event

    def update(self, instance: Event, validated_data: dict) -> Event:
        tags = validated_data.pop('tags', None)
        assigned_to = validated_data.pop('assigned_to_ids', None)

        # Delete RecurringEvent instance if is_recurring is set from True to False
        if not validated_data.get('is_recurring', True) and hasattr(instance, 'recurring_event'):
            instance.recurring_event.delete()

        # Update standard model fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update tags field
        if tags is not None:
            instance.tags.set(tags)

        # Update assigned_to field
        if assigned_to is not None:
            assigned_to_users = User.objects.filter(id__in=assigned_to)
            instance.assigned_to.set(assigned_to_users)
            instance.assigned_to.set(assigned_to_users)

        return instance


class EventDetailSerializer(serializers.ModelSerializer):
    priority = serializers.CharField(source='get_priority_display', read_only=True)
    tags = TagListSerializerField()
    created_by = UserSerializer(read_only=True)
    assigned_to = UserSerializer(many=True, read_only=True)
    recurring_event = RecurringEventSerializer(read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['id', 'created_by', 'title', 'description',
                  'start_datetime', 'location', 'link',
                  'priority', 'image_url', 'tags', 'assigned_to',
                  'is_recurring', 'recurring_event']

    def get_image_url(self, obj: Event) -> str | None:
        if obj.image:
            return f"http://localhost:8080{obj.image.url}"
        return None
