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


file : views.py
project : webometrics

"""
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from core.comm import ScrapydCommunicator
from ..mixins import SecurityMixin
from .serializers import ProjectSerializer, ProjectDomainSerializer, UserSerializer
from webui.models import Project, ProjectDomain


class UserViewSet(SecurityMixin, ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProjectViewSet(SecurityMixin, ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDomainViewSet(SecurityMixin, ModelViewSet):
    queryset = ProjectDomain.objects.all()
    serializer_class = ProjectDomainSerializer

    def pre_save(self, obj):
        obj.creator = self.request.user
        comm = ScrapydCommunicator()
        domain = obj.domain.domain
        if obj.subdomain not in (None, ''):
            domain = obj.subdomain + '.' + domain
        ans = comm.schedule(obj.starturl, domain)
        if ans['status'] == 'ok':
            obj.jobid = ans['jobid']
            obj.status = 'running'
