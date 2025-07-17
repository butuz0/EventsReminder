from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import RegistrationCard


class RegistrationCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationCard
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at')

    def validate_edrpou_code(self, value):
        if not value.isdigit():
            raise ValidationError({'edrpou_code': 'Код ЄДРПОУ повинен містити лише цифри.'})
        if len(value) != 8:
            raise ValidationError({'edrpou_code': 'Код ЄДРПОУ повинен складатись із 8-ми цифр.'})
        return value
