from django.conf.urls import (patterns, url, include)

from .api import CrawlerProjectResource

c = CrawlerProjectResource()

urlpatterns = patterns('',
                       url(r'^api/', include(c.urls)),
)
