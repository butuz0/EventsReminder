from .models import Faculty, Department
from rest_framework import serializers


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['id', 'faculty_name', 'faculty_abbreviation']
  
  
class DepartmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'department_name', 'department_abbreviation', 'faculty']
