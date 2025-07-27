from django.utils.timezone import now
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from apps.events.models import Event
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField()
    object_id = serializers.UUIDField()
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id', 'content_type', 'object_id', 'notification_method',
            'created_by', 'notification_datetime', 'is_sent'
        ]
        read_only_fields = ['id', 'created_by', 'is_sent']

    def get_created_by(self, obj: Notification) -> str:
        return str(obj.created_by.id)

    def validate_notification_datetime(self, value):
        if value < now():
            raise serializers.ValidationError('Нагадування не може бути у минулому.')
        return value

    def validate_content_type(self, value: str) -> ContentType:
        try:
            content_type = ContentType.objects.get(model=value.lower())
        except ContentType.DoesNotExist:
            raise serializers.ValidationError({'content_type': 'Вказаний тип обʼєкта не підтримується.'})

        return content_type

    def validate(self, attrs):
        model_class = attrs.get('content_type').model_class()
        object_id = attrs.get('object_id')
        user = self.context['request'].user

        try:
            obj = model_class.objects.get(id=object_id)
        except model_class.DoesNotExist:
            raise serializers.ValidationError({'object_id': 'Обʼєкт не знайдено.'})

        if model_class is Event:
            if hasattr(obj, 'start_datetime') and attrs['notification_datetime'] > obj.start_datetime:
                raise serializers.ValidationError('Нагадування повинно бути раніше події.')

            if obj.created_by != user and not obj.assigned_to.filter(id=user.id).exists():
                raise serializers.ValidationError('Ви не можете створити нагадування для цієї події.')

        if (attrs['notification_method'] == Notification.NotificationMethod.TELEGRAM
                and not user.profile.is_telegram_verified()):
            raise serializers.ValidationError('Ваш акаунт Telegram не підключено.')

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        return Notification.objects.create(created_by=user, **validated_data)
