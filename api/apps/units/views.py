from django.db.models import QuerySet
from .models import Faculty, Department
from .serializers import DepartmentsSerializer, FacultySerializer, FacultyListSerializer
from apps.common.renderers import JSONRenderer
from rest_framework import generics, permissions


class FacultyListAPIView(generics.ListAPIView):
    serializer_class = FacultyListSerializer
    queryset = Faculty.objects.all()
    permission_classes = [permissions.AllowAny]
    renderer_classes = [JSONRenderer]
    object_label = 'faculties'


class FacultyDetailAPIView(generics.RetrieveAPIView):
    serializer_class = FacultySerializer
    queryset = Faculty.objects.all()
    permission_classes = [permissions.AllowAny]
    pagination_class = None
    lookup_url_kwarg = 'faculty_id'
    lookup_field = 'id'


class DepartmentListAPIView(generics.ListAPIView):
    serializer_class = DepartmentsSerializer
    queryset = Department.objects.all()
    permission_classes = [permissions.AllowAny]
    renderer_classes = [JSONRenderer]
    object_label = 'departments'


class DepartmentDetailAPIView(generics.RetrieveAPIView):
    serializer_class = DepartmentsSerializer
    queryset = Department.objects.all()
    permission_classes = [permissions.AllowAny]
    renderer_classes = [JSONRenderer]
    object_label = 'department'
    lookup_url_kwarg = 'department_id'
    lookup_field = 'id'


class DepartmentsByFacultyAPIView(generics.ListAPIView):
    serializer_class = DepartmentsSerializer
    permission_classes = [permissions.AllowAny]
    renderer_classes = [JSONRenderer]
    object_label = 'departments'

    def get_queryset(self) -> QuerySet[Department, Department]:
        faculty_id = self.kwargs.get('faculty_id')
        return Department.objects.filter(faculty__id=faculty_id)
