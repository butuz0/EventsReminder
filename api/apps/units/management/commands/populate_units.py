from django.core.management.base import BaseCommand
from apps.units.models import Faculty, Department
from pathlib import Path
import json


class Command(BaseCommand):
    help = 'Populate Faculty and Department tables from JSON file'

    def handle(self, *args, **kwargs):
        data_file = Path(__file__).resolve().parent.parent.parent / 'data' / 'units.json'
        with open(data_file, encoding='utf-8') as file:
            data = json.load(file)

        for faculty_data in data:
            faculty, _ = Faculty.objects.get_or_create(
                faculty_name=faculty_data['faculty_name'],
                faculty_abbreviation=faculty_data['faculty_abbreviation']
            )

            for dept in faculty_data['departments']:
                Department.objects.get_or_create(
                    faculty=faculty,
                    department_name=dept['department_name'],
                    department_abbreviation=dept['department_abbreviation']
                )

        self.stdout.write(self.style.SUCCESS('Faculty and Department tables populated successfully.'))
