# -*- coding: utf-8 -*-
"""
    Настройки среды для разработки
"""
from . import *  # NOQA


ALLOWED_HOSTS = ['{{ project_name }}.dev']

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
        'HOST': 'mysql.local',
        'PORT': '3306',
        'TEST_CHARSET': 'utf8',
    }
}

INSTALLED_APPS += (  # NOQA
    'debug_toolbar',
)

MIDDLEWARE = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
) + MIDDLEWARE  # NOQA


def show_toolbar(request):
    if request.is_ajax():
        return False
    return True

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': '{{ project_name }}.settings.develop.show_toolbar',
}
