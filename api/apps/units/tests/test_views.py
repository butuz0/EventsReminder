from django.urls import reverse
from apps.units.models import Department
from apps.units.serializers import DepartmentsSerializer
from .factories import FacultyFactory, DepartmentFactory
import pytest


@pytest.mark.django_db
def test_departments_by_faculty(client):
    faculty = FacultyFactory()
    other_faculty = FacultyFactory()

    DepartmentFactory.create_batch(2, faculty=faculty)
    DepartmentFactory(faculty=other_faculty)

    url = reverse('departments-by-faculty', kwargs={'faculty_id': faculty.id})
    response = client.get(url)

    assert response.status_code == 200
    data = response.json().get('departments').get('results')

    expected_data = DepartmentsSerializer(
        Department.objects.filter(faculty=faculty), many=True
    ).data

    assert data == expected_data
    assert all(d['faculty'] == faculty.id for d in data)
