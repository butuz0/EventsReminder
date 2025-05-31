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
    position = serializers.ReadOnlyField(source='profile.position')
    department = serializers.ReadOnlyField(source='profile.department.department_abbreviation')
    faculty = serializers.ReadOnlyField(source='profile.department.faculty.faculty_abbreviation')

    class Meta(UserSerializer.Meta):
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'full_name',
                  'position', 'department', 'faculty']
        read_only_fields = ['id', 'email']
