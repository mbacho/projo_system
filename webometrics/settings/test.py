"""
Testing django settings for webometrics project.
"""

from .develop import *

DEBUG = True

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

MONGO_DB = {
    'name': 'webometrics_test',
    'link_collection': 'links',
    'outlink_collection': 'outlinks',
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
    "--cover-package=api,core,crawler_server,johnnywalker,stats,webui",
    "--with-fixture-bundling"
]

#celery settings
BROKER_BACKEND = 'memory'
CELERY_ALWAYS_EAGER = True  # skip daemonizing process
