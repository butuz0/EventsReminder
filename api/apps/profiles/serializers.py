from apps.units.models import Department
from .models import Profile
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField


class BaseProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    phone_number = PhoneNumberField()
    telegram_username = serializers.CharField(source='telegram.telegram_username')
    telegram_phone_number = PhoneNumberField(source='telegram.telegram_phone_number')

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'position',
                  'phone_number', 'telegram_username',
                  'telegram_phone_number']


class ProfileSerializer(BaseProfileSerializer):
    id = serializers.UUIDField(source='user.id', read_only=True)
    email = serializers.ReadOnlyField(source='user.email')
    gender = serializers.CharField(source='get_gender_display')
    is_telegram_verified = serializers.CharField(read_only=True)
    department = serializers.SerializerMethodField()
    department_abbreviation = serializers.SerializerMethodField()
    faculty = serializers.SerializerMethodField()
    faculty_abbreviation = serializers.SerializerMethodField()

    class Meta(BaseProfileSerializer.Meta):
        fields = (BaseProfileSerializer.Meta.fields +
                  ['is_telegram_verified', 'id', 'email', 'gender', 
                   'department', 'department_abbreviation', 
                   'faculty', 'faculty_abbreviation'])

    def get_department(self, obj: Profile) -> str:
        if obj.department:
            return obj.department.department_name
        return None

    def get_department_abbreviation(self, obj: Profile) -> str:
        if obj.department:
            return obj.department.department_abbreviation
        return None

    def get_faculty(self, obj: Profile) -> str:
        if obj.department and obj.department.faculty:
            return obj.department.faculty.faculty_name
        return None

    def get_faculty_abbreviation(self, obj: Profile) -> str:
        if obj.department and obj.department.faculty:
            return obj.department.faculty.faculty_abbreviation
        return None


class ProfileUpdateSerializer(BaseProfileSerializer):
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    gender = serializers.ChoiceField(choices=Profile.Gender.choices)

    class Meta(BaseProfileSerializer.Meta):
        fields = BaseProfileSerializer.Meta.fields + ['gender', 'department']

    def update(self, instance: Profile, validated_data: dict) -> Profile:
        user_data = validated_data.pop('user', {})
        telegram_data = validated_data.pop('telegram', {})

        # update standard User model fields
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()

        # update TelegramData model fields
        for attr, value in telegram_data.items():
            setattr(instance.telegram, attr, value)
        instance.telegram.save()

        return super().update(instance, validated_data)
