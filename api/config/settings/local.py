from .base import *  # noqa
from .base import BASE_DIR
from os import path, getenv
from dotenv import load_dotenv


local_env_file = path.join(BASE_DIR, '.envs', '.env.local')

if path.isfile(local_env_file):
    load_dotenv(local_env_file)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SITE_NAME = getenv('SITE_NAME')

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
]

ADMIN_URL = getenv('DJANGO_ADMIN_URL')