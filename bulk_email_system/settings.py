
import os
from pathlib import Path

import environ
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = 'your-secret-key'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'campaigns',
    'rest_framework',
    'django_extensions'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'bulk_email_system.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'campaigns', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bulk_email_system.wsgi.application'

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env("DB_NAME"),
            'USER': env("DB_USER"), 
            'PASSWORD': env("DB_PASSWORD"),
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp-relay.brevo.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
