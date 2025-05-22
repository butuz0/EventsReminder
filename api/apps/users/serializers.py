from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

User = get_user_model()


class CreateUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ['id', 'first_name', 'last_name', 'password']


class CustomUserSerializer(UserSerializer):
    gender = serializers.SerializerMethodField()
    position = serializers.ReadOnlyField(source='profile.position')
    department = serializers.ReadOnlyField(source='profile.department.department_abbreviation')
    faculty = serializers.ReadOnlyField(source='profile.department.faculty.faculty_abbreviation')
    phone_number = PhoneNumberField(source='profile.phone_number')

    def get_gender(self, obj) -> str | None:
        return obj.profile.get_gender_display()

    class Meta(UserSerializer.Meta):
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'full_name',
                  'gender', 'position', 'department', 'faculty', 'phone_number']
        read_only_fields = ['id', 'email']
