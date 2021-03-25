"""
Django settings for yandex_backend_task project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7s&jf!5-y0tl6nxk9&e!9!@%jx=a6egk4a#mf5-@@)&zzzq@%y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'main',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
]

ROOT_URLCONF = 'yandex_backend_task.urls'


WSGI_APPLICATION = 'yandex_backend_task.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'yandex_backend_task',
        'USER' : 'yandex',
        'PASSWORD' : '123456',
        'HOST' : 'db',
        'PORT' : '5432',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

