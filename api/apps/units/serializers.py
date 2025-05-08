from .models import Faculty, Department
from apps.profiles.models import Profile
from rest_framework import serializers


class FacultySerializer(serializers.ModelSerializer):
    num_employees = serializers.SerializerMethodField()

    class Meta:
        model = Faculty
        fields = ['id', 'faculty_name', 'faculty_abbreviation',
                  'num_employees']

    def get_num_employees(self, obj: Faculty) -> int:
        return Profile.objects.filter(department__faculty=obj).count()


class DepartmentsSerializer(serializers.ModelSerializer):
    num_employees = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ['id', 'department_name', 'department_abbreviation',
                  'faculty', 'num_employees']

    def get_num_employees(self, obj: Department) -> int:
        return Profile.objects.filter(department=obj).count()
