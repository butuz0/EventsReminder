import django
from pathlib import Path
import sys
import os


def setup_django():
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    sys.path.append(str(BASE_DIR / 'api'))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
    django.setup()
