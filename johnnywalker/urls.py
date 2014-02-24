from django.conf.urls import (patterns, include, url)


urlpatterns = patterns('',
                       url('^api/', include('johnnywalker.api.urls')),

)
