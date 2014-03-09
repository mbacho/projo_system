from django.conf.urls import (patterns, include, url)
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),

                       url(r'', include('webui.urls')),
                       url(r'', include('johnnywalker.urls')),
                       url(r'', include('stats.urls')),
                       url(r'^api/', include('api.urls')),
                       url(r'^', include('crawler_server.urls')),
)
