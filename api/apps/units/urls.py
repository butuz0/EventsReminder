from django.urls import path
from .views import (
    FacultyListAPIView,
    DepartmentListAPIView,
    DepartmentsByFacultyAPIView
)

urlpatterns = [
    path('all-faculties/', FacultyListAPIView.as_view(), name='faculty-list'),
    path('all-departments/', DepartmentListAPIView.as_view(), name='department-list'),
    path('faculty/<int:faculty_id>/departments/', DepartmentsByFacultyAPIView.as_view(), name='departments-by-faculty'),
]
