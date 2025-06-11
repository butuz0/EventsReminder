from django.contrib import admin
from .models import Faculty, Department


class DepartmentInline(admin.StackedInline):
    model = Department
    extra = 0
    verbose_name = 'Department'
    verbose_name_plural = 'Departments'


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['id', 'faculty_name', 'faculty_abbreviation']
    list_display_links = ['id', 'faculty_name']
    search_fields = ['faculty_name', 'faculty_abbreviation']
    inlines = [DepartmentInline]


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    def faculty_abbreviation(self, obj: Department) -> str:
        return obj.faculty.faculty_abbreviation

    faculty_abbreviation.short_description = 'Faculty Abbreviation'

    list_display = ['id', 'department_name', 'department_abbreviation', 'faculty_abbreviation']
    list_display_links = ['id', 'department_name']
    search_fields = ['department_name', 'department_abbreviation']
