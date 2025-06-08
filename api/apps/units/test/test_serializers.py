from .factories import FacultyFactory, DepartmentFactory
from apps.profiles.tests.factories import ProfileFactory
from apps.units.serializers import DepartmentsSerializer, FacultySerializer, FacultyListSerializer
import pytest


@pytest.mark.django_db
def test_departments_serializer(super_user):
    department = DepartmentFactory()

    ProfileFactory.create_batch(3, department=department)
    ProfileFactory(department=department, user=super_user)

    serializer = DepartmentsSerializer(instance=department)
    data = serializer.data

    assert data['num_employees'] == 3
    assert data['department_name'] == department.department_name
    assert data['faculty'] == department.faculty.id


@pytest.mark.django_db
def test_faculty_serializer(super_user):
    faculty = FacultyFactory()
    dep1 = DepartmentFactory(faculty=faculty)
    dep2 = DepartmentFactory(faculty=faculty)

    serializer = FacultySerializer(instance=faculty)
    data = serializer.data

    assert data['faculty_name'] == faculty.faculty_name
    assert len(data['departments']) == 2

    department_ids = [dep1.id, dep2.id]
    for department in data['departments']:
        assert department['id'] in department_ids


@pytest.mark.django_db
def test_faculty_list_serializer(super_user):
    faculty = FacultyFactory()
    dep1 = DepartmentFactory(faculty=faculty)
    dep2 = DepartmentFactory(faculty=faculty)

    ProfileFactory.create_batch(3, department=dep1)
    ProfileFactory.create_batch(5, department=dep2)
    ProfileFactory(department=dep1, user=super_user)

    serializer = FacultyListSerializer(instance=faculty)
    data = serializer.data

    assert data['num_employees'] == 8
    assert data['faculty_name'] == faculty.faculty_name
