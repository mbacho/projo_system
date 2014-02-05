"""
Testing django settings for webometrics project.
"""

from .develop import *

#In memory database for testing
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}

INSTALLED_APPS += (
    'django_nose',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    "--with-coverage",
    "--cover-branches",
    "--cover-html",
    "--cover-html-dir=coverage_html_reports",
    "--cover-erase",
    "--cover-package=core,johnnywalker,stats,webui"
]