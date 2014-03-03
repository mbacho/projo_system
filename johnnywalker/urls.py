from django.conf.urls import (patterns, url)
from .views import home

urlpatterns = patterns('',
                       url(r'^crawler/', home, name='crawler-home'),
)
