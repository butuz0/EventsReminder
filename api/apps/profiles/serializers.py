from multiprocessing import Value
from apps.units.models import Department
from .models import Profile, TelegramData
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField


class BaseProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    avatar = serializers.ImageField(write_only=True, required=False)
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'position',
                  'avatar', 'avatar_url']

    def get_avatar_url(self, obj: Profile) -> str | None:
        request = self.context.get('request')
        if obj.avatar and request:
            url = request.build_absolute_uri(obj.avatar.url)
            if url.startswith('http://localhost/'):
                return url.replace('http://localhost/', 'http://localhost:8080/')
            return url
        return None


class TelegramDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramData
        fields = ['telegram_username', 'telegram_first_name',
                  'telegram_last_name', 'is_verified']


class ProfileRetrieveSerializer(BaseProfileSerializer):
    id = serializers.UUIDField(source='user.id', read_only=True)
    email = serializers.ReadOnlyField(source='user.email')
    department_name = serializers.SerializerMethodField()
    department_abbreviation = serializers.SerializerMethodField()
    faculty = serializers.SerializerMethodField()
    faculty_abbreviation = serializers.SerializerMethodField()
    telegram = TelegramDataSerializer()

    class Meta(BaseProfileSerializer.Meta):
        fields = (BaseProfileSerializer.Meta.fields +
                  ['id', 'email', 'department', 'department_name',
                   'department_abbreviation', 'faculty',
                   'faculty_abbreviation', 'telegram'])

    def get_department_name(self, obj: Profile) -> str | None:
        if obj.department:
            return obj.department.department_name
        return None

    def get_department_abbreviation(self, obj: Profile) -> str | None:
        if obj.department:
            return obj.department.department_abbreviation
        return None

    def get_faculty(self, obj: Profile) -> str | None:
        if obj.department and obj.department.faculty:
            return obj.department.faculty.faculty_name
        return None

    def get_faculty_abbreviation(self, obj: Profile) -> str | None:
        if obj.department and obj.department.faculty:
            return obj.department.faculty.faculty_abbreviation
        return None


class ProfileUpdateSerializer(BaseProfileSerializer):
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())

    class Meta(BaseProfileSerializer.Meta):
        fields = BaseProfileSerializer.Meta.fields + ['department']

    def update(self, instance: Profile, validated_data: dict) -> Profile:
        user_data = validated_data.pop('user', {})

        # update standard User model fields
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()

        return super().update(instance, validated_data)


class ProfileSetupSerializer(serializers.ModelSerializer):
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())

    class Meta:
        model = Profile
        fields = ['position', 'department']
