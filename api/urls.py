"""
The MIT License

Copyright (c) 2014, mbacho (Chomba Ng'ang'a)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.


file : urls.py
project : webometrics

"""
from django.conf.urls import url, include, patterns

from rest_framework.routers import DefaultRouter
from .webui.views import UserViewSet, ProjectViewSet, ProjectDomainViewSet
from .stats.views import DomainStatsViewSet
from .johnnywalker.views import AcademicDomainViewSet, AvoidUrlViewSet

router = DefaultRouter()

router.register(r'projects', ProjectViewSet)
router.register(r'users', UserViewSet)
router.register(r'projectdomains', ProjectDomainViewSet)

router.register(r'domainstats', DomainStatsViewSet)

router.register(r'academicdomains', AcademicDomainViewSet)
router.register(r'avoidurls', AvoidUrlViewSet)

urlpatterns = patterns('',
                       url(r'^', include(router.urls)),
                       url(r'^api-docs/', include('rest_framework_swagger.urls')),
)
