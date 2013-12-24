from django.conf.urls import patterns, include, url
from views import home

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webometrics.views.home', name='home'),
    # url(r'^webometrics/', include('webometrics.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'',home,name='home'),

    url(r'signup',home,name='signup'),
    url(r'login',home,name='signin'),
    url(r'logout',home,name='signout'),

    url(r'projects',home,name='project_list'),

    url(r'project/create',home,name='project_new'),
    url(r'project/edit',home,name='project_edit'),
    url(r'project/del',home,name='project_del'),

    url(r'project/stats',home,name='project_stats'),
)
