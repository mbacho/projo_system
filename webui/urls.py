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

                       url(r'^results/', home, name='results'),

                       url(r'^user/', home, name='user'),
)
