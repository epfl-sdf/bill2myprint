"""
Django settings for django_example project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import json
import os

from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# helper functions to get absolute paths
def path_from_root(*x):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', *x))


BASE_DIR = path_from_root('')


with open(path_from_root("../../bill2myprint.secrets.json"), 'r') as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} environnement variable".format(setting)
        raise ImproperlyConfigured(error_msg)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bill2myprint',
    'uniflow',
    'equitrac',
    'userprofile',
    'django_tequila',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_tequila.middleware.TequilaMiddleware',
]

AUTHENTICATION_BACKENDS = ('django_tequila.django_backend.TequilaBackend',)
TEQUILA_SERVICE_NAME = "Bill2myprint and Tequila"
LOGIN_URL = "/login"
LOGIN_REDIRECT_URL = "/logged"
LOGIN_REDIRECT_IF_NOT_ALLOWED = "/not_allowed"
LOGOUT_URL = "/"
TEQUILA_NEW_USER_INACTIVE = True

AUTH_PROFILE_MODULE = "userprofile"

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR + '/templates'
        ],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bill2myprint',
	'HOST': '127.0.0.1',
        'USER': 'bill2myprint',
        'PASSWORD': get_secret('OUR_DB_PASSWORD'),
    },
    'myprint': {
        'ENGINE': 'sql_server.pyodbc',
        'HOST': 'mssql-tst-uat.epfl.ch',
        'NAME': 'DsPcDb_TEST',
        'USER': 'build2myprint',
        'PASSWORD': get_secret('MYPRINT_DB_PASSWORD'),
        'PORT': 1433,
        'OPTIONS': {
            'driver': 'FreeTDS',
            'host_is_server': True,
            'extra_params': "TDS_VERSION=7.4"
        }
    },
    # Beware that the account used here must have access to the database for this to work
    # 'equitrac_transactions': {
    #     'ENGINE': 'sql_server.pyodbc',
    #     'HOST': 'mssql-tst-uat.epfl.ch',
    #     'NAME': 'myPrint_eqcas_stats',
    #     'USER': 'INTRANET\username_tequila_gaspar',
    #     'PASSWORD': 'password_tequila',
    #     'PORT': 1433,
    #     'OPTIONS': {
    #         'driver': 'FreeTDS',
    #         'host_is_server': True,
    #         'extra_params': "TDS_VERSION=8.0"
    #     }
    # },
    # 'semesters_db': {
    #     'ENGINE': 'sql_server.pyodbc',
    #     'HOST': 'mssql-tst-uat.epfl.ch',
    #     'NAME': 'myPrint_Accounts',
    #     'USER': 'INTRANET\username_tequila_gaspar',
    #     'PASSWORD': 'password_tequila',
    #     'PORT': 1433,
    #     'OPTIONS': {
    #         'driver': 'FreeTDS',
    #         'host_is_server': True,
    #         'extra_params': "TDS_VERSION=8.0"
    #     }
    # },
}

DATABASE_ROUTERS = ['config.dbrouter.MyPrintRouter']


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
