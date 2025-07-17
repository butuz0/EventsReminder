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
            raise serializers.ValidationError('Нагадування не може бути у минулому.')

        event = self.initial_data.get('event')
        if not event:
            raise serializers.ValidationError('Подію не було надано.')

        try:
            event = Event.objects.select_related('recurring_event').get(id=event)
        except Event.DoesNotExist:
            raise serializers.ValidationError('Подія не існує.')

        if value > event.start_datetime:
            raise serializers.ValidationError('Нагадування повинно бути раніше події.')

        return value

    def validate_event(self, value):
        if not Event.objects.filter(id=value).exists():
            raise serializers.ValidationError('Подія не існує.')
        return value

    def validate(self, attrs):
        event_id = attrs.get('event')
        event = Event.objects.get(id=event_id)
        user = self.context['request'].user

        if event.created_by != user and not event.assigned_to.filter(id=user.id).exists():
            raise serializers.ValidationError('Ви не можете створити нагадування для цієї події.')

        if (attrs.get(
                'notification_method') == Notification.NotificationMethod.TELEGRAM and not user.profile.is_telegram_verified()):
            raise serializers.ValidationError('Ваш акаунт Telegram не підключено.')

        return attrs

    def create(self, validated_data):
        event_id = validated_data.pop('event')
        event = Event.objects.get(id=event_id)
        user = self.context['request'].user

        return Notification.objects.create(event=event, created_by=user, **validated_data)
