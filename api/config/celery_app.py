from django.conf import settings
from celery import Celery
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

app = Celery('kpi_remind')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
