from django.db import models
from django.utils.translation import gettext_lazy as _


class Faculty(models.Model):
    faculty_name = models.CharField(verbose_name=_('Faculty Name'), max_length=250, unique=True)
    faculty_abbreviation = models.CharField(verbose_name=_('Faculty Аbbreviation'), max_length=20, unique=True)

    class Meta:
        verbose_name = _('Faculty')
        verbose_name_plural = _('Faculties')

    def __str__(self) -> str:
        return f'{self.faculty_name} - {self.faculty_abbreviation}'


class Department(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, related_name='departments')
    department_name = models.CharField(verbose_name=_('Department Name'), max_length=250, unique=True)
    department_abbreviation = models.CharField(verbose_name=_('Department Аbbreviation'), max_length=20)

    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')

    def __str__(self) -> str:
        faculty_name = self.faculty.faculty_abbreviation if self.faculty else 'No Faculty'
        return f'{self.department_name} - {self.department_abbreviation} ({faculty_name})'
