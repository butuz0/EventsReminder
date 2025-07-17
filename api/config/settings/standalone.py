from .base import *  # noqa
from .base import BASE_DIR
from os import path, getenv
from dotenv import load_dotenv

stand_env_file = path.join(BASE_DIR, '.envs', '.env.standalone')

if path.isfile(stand_env_file):
    load_dotenv(stand_env_file)

SECRET_KEY = getenv('DJANGO_SECRET_KEY')

DEBUG = False

MEDIA_URL = '/media/'
MEDIA_ROOT = str(BASE_DIR / 'media')

SITE_NAME = getenv('SITE_NAME')

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    '.ngrok-free.app'
]

CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8080',
    'http://localhost:8080',
]

ADMIN_URL = getenv('DJANGO_ADMIN_URL')

ADMINS = [
    ('Yaroslav Oryshchenko', 'y.o.oryshchenko@gmail.com'),
]

EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
EMAIL_HOST = getenv('EMAIL_HOST')
EMAIL_PORT = getenv('EMAIL_PORT')
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST_USER = getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = getenv('DEFAULT_FROM_EMAIL')
SERVER_EMAIL = getenv('DEFAULT_FROM_EMAIL')
DOMAIN = getenv('DOMAIN')

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SECURE_SSL_REDIRECT = getenv('DJANGO_SECURE_SSL_REDIRECT', 'True') == 'True'

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

SECURE_HSTS_SECONDS = 300

SECURE_HSTS_INCLUDE_SUBDOMAINS = (
        getenv('DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', 'True') == 'True'
)

SECURE_HSTS_PRELOAD = getenv('DJANGO_SECURE_HSTS_PRELOAD', 'True') == 'True'

SECURE_CONTENT_TYPE_NOSNIFF = (
        getenv('DJANGO_SECURE_CONTENT_TYPE_NOSNIFF', 'True') == 'True'
)
