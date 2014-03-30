"""
Production django settings for webometrics project.
"""

from os import getenv

from .base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd2itcuic6n4g8d',
        'USER': 'tzgiqrvzdmayuo',
        'PASSWORD': 'wxCQ6V_k8DVh0K2Qbd5UI0rIzn',
        'HOST': 'ec2-23-21-101-129.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}

EMAIL_HOST = getenv('MAILTRAP_HOST')
EMAIL_HOST_USER = getenv('MAILTRAP_USER_NAME')
EMAIL_HOST_PASSWORD = getenv('MAILTRAP_PASSWORD')
EMAIL_PORT = getenv('MAILTRAP_PORT')
EMAIL_USE_TLS = False

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# MONGODB_URL = 'mongodb://webometrics:pass@oceanic.mongohq.com:10095/webometrics'

# REDIS_URL = 'redis://redistogo:712486db5b7fc6f02b5282f6340e5883@grideye.redistogo.com:10222/'

