"""
Production django settings for webometrics project.
"""

from .base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

#TODO: Hide secret keys e.g. using environment variables
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'webometrics', # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'webometrics',
        'PASSWORD': 'pass',
        'HOST': '', # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '', # Set to empty string for default.
    }
}
