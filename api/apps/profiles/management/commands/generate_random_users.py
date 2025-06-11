from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.units.models import Department
from faker import Faker
import random

User = get_user_model()
fake = Faker('uk_UA')

departments = list(Department.objects.all())
positions = [
    'Професор', 'Доцент', 'Асистент', 'Лаборант', 'Старший викладач',
    'Молодший викладач', 'Науковий працівник', 'Методист'
]


class Command(BaseCommand):
    help = 'Populate user model with randomly generated users'

    def handle(self, *args, **kwargs):
        created = 0
        for _ in range(200):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = f'{fake.unique.user_name()}@kpi.ua'
            password = 'Pass123456'

            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
            )

            user.refresh_from_db()

            user.profile.department = random.choice(departments)
            user.profile.position = random.choice(positions)
            user.profile.save()

            created += 1

        print(f'Створено {created} користувачів')
