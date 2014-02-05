from django.conf.urls import (patterns, url)
from .views import home

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'webometrics.views.home', name='home'),
                       # url(r'^webometrics/', include('webometrics.foo.urls')),

                       url(r'^$', home, name='home'),

                       url(r'^signup/', home, name='signup'),
                       url(r'^login/', home, name='signin'),
                       url(r'^logout/', home, name='signout'),

                       url(r'^projects/', home, name='project_list'),
                       url(r'^project/create', home, name='project_new'),
                       url(r'^project/edit', home, name='project_edit'),
                       url(r'^project/del', home, name='project_del'),
                       url(r'^project/stats', home, name='project_stats'),

                       url(r'user', home, name='user'),
)
