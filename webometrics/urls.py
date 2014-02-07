

from django.conf.urls import (patterns, include, url)
from django.contrib import admin
from johnnywalker.api import CrawlerProjectResource
from stats.api import ResultsResource
from webui.api import UserProjectResource
from tastypie.api import Api

admin.autodiscover()

api = Api(api_name='api')
api.register(CrawlerProjectResource())
api.register(ResultsResource())
api.register(UserProjectResource())

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'webometrics.views.home', name='home'),
                       # url(r'^webometrics/', include('webometrics.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),

                       url(r'', include('webui.urls')),
                       url(r'', include('johnnywalker.urls')),
                       url(r'', include('stats.urls')),
                       url(r'',include(api.urls))
)
