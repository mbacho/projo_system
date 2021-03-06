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
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from crawler_server.tasks import RunSpider
from ..mixins import SecurityMixin
from .serializers import ProjectSerializer, ProjectDomainSerializer, UserSerializer
from stats.miner import Miner
from webui.models import Project, ProjectDomain


class UserViewSet(SecurityMixin, ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProjectViewSet(SecurityMixin, ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def pre_save(self, obj):
        obj.owner = self.request.user


class ProjectDomainViewSet(SecurityMixin, ModelViewSet):
    queryset = ProjectDomain.objects.all()
    serializer_class = ProjectDomainSerializer

    def pre_save(self, obj):
        if obj.starturl == '':
            obj.starturl = obj.domain.link

        if not obj.jobid:
            rs = RunSpider()
            result = rs.delay(domain=obj.get_crawl_domain, starturl=obj.starturl)
            obj.jobid = result.task_id
            if result.status == 'PENDING':
                obj.status = 'running'

    def pre_delete(self, obj):
        pass

    @action(methods=['POST'])
    def pagerank(self, request, pk):
        pd = ProjectDomain.objects.get(id=pk)
        miner = Miner(pd.jobid, pd)
        pr = miner.pagerank()
        return Response(pr)

    @action()
    def canceljob(self, request, pk):
        pd = ProjectDomain.objects.get(id=pk)
        if request.user.is_superuser or pd.project.owner == request.user:
            #TODO check if job belongs to current user or is admin
            return Response({'status': 'ok'})
        else:
            return Response({'error': 'Unauthorized action'}, HTTP_401_UNAUTHORIZED)

