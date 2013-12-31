"""
Testing django settings for webometrics project.
"""

from .develop import *

#TODO : hide secrets
DATABASES['default']['USER'] = 'barbossa'
DATABASES['default']['PASSWORD'] = 'paswad'

INSTALLED_APPS += (
    'django_nose',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
