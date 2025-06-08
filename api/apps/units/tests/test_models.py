from .factories import FacultyFactory, DepartmentFactory
import pytest


@pytest.mark.django_db
def test_faculty_str():
    faculty = FacultyFactory(
        faculty_name='Test Faculty 1',
        faculty_abbreviation='TF1'
    )
    assert str(faculty) == 'Test Faculty 1 - TF1'


@pytest.mark.django_db
def test_department_str():
    department = DepartmentFactory(
        department_name='Test Department 1',
        department_abbreviation='TD1',
        faculty__faculty_abbreviation='TF1'
    )
    assert str(department) == 'Test Department 1 - TD1 (TF1)'


@pytest.mark.django_db
def test_department_no_faculty_str():
    department = DepartmentFactory(
        department_name='Test Department 1',
        department_abbreviation='TD1',
        faculty=None
    )
    assert str(department) == 'Test Department 1 - TD1 (No Faculty)'


@pytest.mark.django_db
def test_faculty_delete():
    department = DepartmentFactory(
        department_name='Test Department 2',
        department_abbreviation='TD2',
    )
    department.faculty.delete()
    department.refresh_from_db()

    assert department.faculty is None
    assert str(department) == 'Test Department 2 - TD2 (No Faculty)'
