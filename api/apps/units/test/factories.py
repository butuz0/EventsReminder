from apps.units.models import Faculty, Department
from faker import Factory
import factory

faker = Factory.create()


class FacultyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Faculty

    faculty_name = factory.LazyAttribute(lambda x: f'Faculty {faker.company()}')
    faculty_abbreviation = factory.LazyAttribute(lambda x: faker.lexify(text='???').upper())


class DepartmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Department

    department_name = factory.LazyAttribute(lambda x: f'Department {faker.company()}')
    department_abbreviation = factory.LazyAttribute(lambda x: faker.lexify(text='???').upper())
    faculty = factory.SubFactory(FacultyFactory)
