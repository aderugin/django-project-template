# -*- coding: utf-8 -*-
"""
    Настройки среды для разработки
"""
from . import *


SITE_ID = 1

DEBUG = True

COMPRESS_ENABLED = not DEBUG

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '{{ project_name }}',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
        'TEST_CHARSET': 'utf8',
    }
}

INSTALLED_APPS += (
    'debug_toolbar',
)
