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


file : serializers.py
project : webometrics

"""
from django.contrib.auth.models import User
from rest_framework.serializers import HyperlinkedModelSerializer, HyperlinkedRelatedField
from webui.models import Project, ProjectDomain


class ProjectDomainSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = ProjectDomain
        fields = (
            'url', 'id', 'project', 'domain', 'starturl', 'subdomain',
            'jobid', 'starttime', 'stoptime', 'status'
        )


class ProjectSerializer(HyperlinkedModelSerializer):
    projectdomain_project = HyperlinkedRelatedField(many=True, view_name='projectdomain-detail', required=False)

    class Meta:
        model = Project
        fields = ('url', 'id', 'name', 'created', 'owner', 'projectdomain_project')


class UserSerializer(HyperlinkedModelSerializer):
    projects = HyperlinkedRelatedField(many=True, view_name='project-detail', required=False)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'email', 'projects')
