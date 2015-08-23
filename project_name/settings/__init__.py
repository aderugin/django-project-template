# -*- coding: utf-8 -*-
"""
    Project settings
"""
import os


#==============================================================================
# Django
#==============================================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECRET_KEY = '{{ secret_key }}'

DEBUG = True

ALLOWED_HOSTS = []

SITE_ID = 1

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = '{{ project_name }}.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
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

WSGI_APPLICATION = '{{ project_name }}.wsgi.application'


# Internationalization

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Asia/Yekaterinburg'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'public', 'media')

STATIC_ROOT = os.path.join(BASE_DIR, 'public' 'static')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)


# Session

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

SESSION_SAVE_EVERY_REQUEST = True

SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 4

SESSION_COOKIE_DOMAIN = None


# Installed apps

INSTALLED_APPS += (
    # Additional apps
    # Project apps
)


#==============================================================================
# Compress
#==============================================================================

COMPRESS_ENABLED = not DEBUG

COMPRESS_OUTPUT_DIR = 'comporess'


#==============================================================================
# Haystack
#==============================================================================

HAYSTACK_XAPIAN_LANGUAGE = 'russian'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'xapian_backend.XapianEngine',
        'PATH': os.path.join(BASE_DIR, 'xapian_index'),
    },
}


#==============================================================================
# Logging
#==============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        '{{ project_name }}.apps': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        '{{ project_name }}.base': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


#==============================================================================
# Thumbnails
#==============================================================================

THUMBNAIL_QUALITY = 100


#==============================================================================
# Django settings app
#==============================================================================

# DJANGO_SETTINGS_MODEL = '{{ project_name }}.base.models.Settings'


#==============================================================================
# Settings imports
#==============================================================================

# Production settings
if os.environ.get('ENV') == 'production':
    from .production import *

# Develop settings
elif os.environ.get('ENV') == 'develop':
    from .develop import *

# Staging settings
elif os.environ.get('ENV') == 'staging':
    from .staging import *

# Default choice
else:
    from .develop import *

# Local settings
try:
    from local.py import *
except ImportError:
    pass