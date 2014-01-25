

from django.conf.urls import (patterns, url)
from .views import home

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'webometrics.views.home', name='home'),
                       # url(r'^webometrics/', include('webometrics.foo.urls')),
                       url(r'^crawler', home, name='crawler_home'),
)
