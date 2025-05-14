from django.urls import path
from .views import (
    FacultyListAPIView,
    FacultyDetailAPIView,
    DepartmentListAPIView,
    DepartmentDetailAPIView,
    DepartmentsByFacultyAPIView
)

urlpatterns = [
    path('all-faculties/', FacultyListAPIView.as_view(), name='faculty-list'),
    path('all-departments/', DepartmentListAPIView.as_view(), name='department-list'),
    path('department/<int:department_id>/', DepartmentDetailAPIView.as_view(), name='department-detail'),
    path('faculty/<int:faculty_id>/', FacultyDetailAPIView.as_view(), name='faculty-detail'),
    path('faculty/<int:faculty_id>/departments/', DepartmentsByFacultyAPIView.as_view(), name='departments-by-faculty'),
]
