from django.utils.timezone import now
from django.contrib.auth import get_user_model
from apps.users.serializers import CustomUserSerializer
from .models import Event, RecurringEvent
from rest_framework import serializers
from taggit.serializers import TagListSerializerField, TaggitSerializer

User = get_user_model()


class RecurringEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringEvent
        fields = [
            'id', 'recurrence_rule', 'recurrence_end_datetime', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class EventSerializer(TaggitSerializer, serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    assigned_to_ids = serializers.ListField(child=serializers.UUIDField(), write_only=True)
    assigned_to = CustomUserSerializer(many=True, read_only=True)
    tags = TagListSerializerField(required=False)
    recurring_event = RecurringEventSerializer(required=False, allow_null=True)

    class Meta:
        model = Event
        fields = [
            'id', 'created_by', 'title', 'description', 'start_datetime', 
            'location', 'link', 'priority', 'image', 'tags', 'created_at', 
            'updated_at', 'assigned_to_ids', 'assigned_to', 'is_recurring', 
            'recurring_event'
        ]
        read_only_fields = ['id', 'created_by', 'assigned_to', 'created_at', 'updated_at']


    def validate_start_datetime(self, value):
        if value < now():
            raise serializers.ValidationError('Event start time cannot be in the past.')
        return value

    def validate_assigned_to_ids(self, value):
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

    def validate(self, attrs):
        is_recurring = attrs.get('is_recurring', False)
        recurring_event_data = attrs.get('recurring_event')
        start_time = attrs.get('start_datetime')

        if is_recurring and not recurring_event_data:
            raise serializers.ValidationError(
                'If you mark the event as recurring, you must provide recurring_event data.'
            )
        if recurring_event_data and not is_recurring:
            raise serializers.ValidationError(
                'If you provide recurrence details, the event must be marked as is_recurring=True.'
            )

        if is_recurring and recurring_event_data:
            end_time = recurring_event_data.get('recurrence_end_datetime')
            if start_time and end_time and end_time < start_time:
                raise serializers.ValidationError(
                    'Recurring event end time must be after the start time.'
                )

        return attrs


    def create(self, validated_data) -> Event:
        tags = validated_data.pop('tags', [])
        assigned_to = validated_data.pop('assigned_to_ids', [])
        recurring_event_data = validated_data.pop('recurring_event', None)  
        
        user = self.context['request'].user
        
        event = Event.objects.create(created_by=user, **validated_data)
        event.tags.set(tags)
        
        assigned_to_users = User.objects.filter(id__in=assigned_to)
        event.assigned_to.set(assigned_to_users)

        if recurring_event_data:
            RecurringEvent.objects.create(event=event, **recurring_event_data)

        return event

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        assigned_to = validated_data.pop('assigned_to', None)
        recurring_event_data = validated_data.pop('recurring_event', None)

        if not validated_data.get('is_recurring', True) and hasattr(instance, 'recurring_event'):
            instance.recurring_event.delete()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tags is not None:
            instance.tags.set(tags)

        if assigned_to is not None:
            instance.assigned_to.set(assigned_to)

        if recurring_event_data:
            if hasattr(instance, 'recurring_event'):
                for key, val in recurring_event_data.items():
                    setattr(instance.recurring_event, key, val)
                instance.recurring_event.save()
            else:
                RecurringEvent.objects.create(event=instance, **recurring_event_data)

        instance.refresh_from_db()
        return instance
