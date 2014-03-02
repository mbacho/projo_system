from django.conf.urls import (patterns, url, include)
from .views import (home, signin, signout, signup, project_new, project_edit, project_del, results)

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'webometrics.views.home', name='home'),
                       # url(r'^webometrics/', include('webometrics.foo.urls')),
                       url(r'^$', home, name='home'),

                       url(r'^signup/', signup, name='signup'),
                       url(r'^signin/', signin, name='signin'),
                       url(r'^signout/', signout, name='signout'),

                       url(r'^projects/', home, name='project_list'),
                       url(r'^project/new/([A-Za-z0-9]+)', project_new, name='project_new'),
                       url(r'^project/edit/([A-Za-z0-9]+)', project_edit, name='project_edit'),
                       url(r'^project/del/([A-Za-z0-9]+)', project_del, name='project_del'),
                       url(r'^project/stats', home, name='project_stats'),

                       url(r'^results/', home, name='results'),

                       url(r'^user/', home, name='user'),
)
