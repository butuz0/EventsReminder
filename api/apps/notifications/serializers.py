from django.utils.timezone import now
from rest_framework import serializers
from apps.events.models import Event
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    event = serializers.UUIDField()
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id', 'event', 'notification_method', 'created_by',
            'notification_datetime', 'is_sent'
        ]
        read_only_fields = ['id', 'created_by', 'is_sent']

    def get_created_by(self, obj: Notification) -> str:
        return str(obj.created_by.id)

    def validate_notification_datetime(self, value):
        if value < now():
            raise serializers.ValidationError('Notification datetime cannot be in the past.')

        event = self.initial_data.get('event')
        if not event:
            raise serializers.ValidationError('Event is required.')

        try:
            event = Event.objects.select_related('recurring_event').get(id=event)
        except Event.DoesNotExist:
            raise serializers.ValidationError('Event does not exist.')

        if value > event.start_datetime:
            raise serializers.ValidationError('Notification must be before event start time.')

        if event.is_recurring and hasattr(event, 'recurring_event'):
            recurrence_end = event.recurring_event.recurrence_end_datetime
            if recurrence_end and value > recurrence_end:
                raise serializers.ValidationError('Notification must be before recurring event end time.')

        return value

    def validate_event(self, value):
        if not Event.objects.filter(id=value).exists():
            raise serializers.ValidationError('Event does not exist.')
        return value

    def validate(self, attrs):
        event_id = attrs.get('event')
        event = Event.objects.get(id=event_id)
        user = self.context['request'].user

        if event.created_by != user and not event.assigned_to.filter(id=user.id).exists():
            raise serializers.ValidationError('You do not have permission to create notifications for this event.')

        if (attrs.get(
                'notification_method') == Notification.NotificationMethod.TELEGRAM and not user.profile.is_telegram_verified()):
            raise serializers.ValidationError('Your Telegram account is not connected yet.')

        return attrs

    def create(self, validated_data):
        event_id = validated_data.pop('event')
        event = Event.objects.get(id=event_id)
        user = self.context['request'].user

        return Notification.objects.create(event=event, created_by=user, **validated_data)
