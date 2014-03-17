from django.conf.urls import (patterns, url )
from .views import (home, signin, signout, signup, user)
from .views import (project, project_edit, project_del)

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'webometrics.views.home', name='home'),
                       # url(r'^webometrics/', include('webometrics.foo.urls')),
                       url(r'^$', home, name='home'),

                       url(r'^signup/', signup, name='signup'),
                       url(r'^signin/', signin, name='signin'),
                       url(r'^signout/', signout, name='signout'),

                       url(r'^project/([0-9]+)/', project, name='project_det'),
                       url(r'^project/edit/', project_edit, name='project_new'),
                       url(r'^project/edit/([0-9]+)/', project_edit, name='project_edit'),
                       url(r'^project/delete/([0-9]+)/', project_del, name='project_delete'),

                       url(r'^projectdomain/new/', home, name='projectdomain_new'),
                       url(r'^projectdomain/edit/([0-9]+)', home, name='projectdomain_edit'),
                       url(r'^projectdomain/delete/([0-9]+)', home, name='projectdomain_delete'),

                       url(r'^results/', home, name='results'),

                       url(r'^user/', user, name='user'),
)
