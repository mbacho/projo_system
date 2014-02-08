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


file : api.py
project : webometrics

"""
from django.contrib.auth.models import User
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import (ModelResource, ALL, ALL_WITH_RELATIONS)
from tastypie.fields import (ForeignKey )
from johnnywalker.models import AcademicDomain
from .models import (Project, ProjectDomain)


class MyBaseModelResource(ModelResource):
    class Meta:
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        allowed_methods = ['get', 'post', 'put', 'delete']


class UserResource(MyBaseModelResource):
    class Meta(MyBaseModelResource.Meta):
        resource_name = 'user'
        queryset = User.objects.all()
        fields = ['email', 'first_name', 'last_name', 'username']
        filtering = {
            'username': ALL
        }


class AcademicDomainResource(MyBaseModelResource):
    class Meta(MyBaseModelResource.Meta):
        resource_name = 'domain'
        queryset = AcademicDomain.objects.all()
        filtering = {
            'domain': ALL
        }


class ProjectResource(MyBaseModelResource):
    owner = ForeignKey(UserResource, 'owner')

    class Meta(MyBaseModelResource.Meta):
        fields = ['name']
        queryset = Project.objects.all()
        resource_name = 'project'
        filtering = {
            'owner': ALL_WITH_RELATIONS,
            'created': ['exact', 'lt', 'lte', 'gt', 'gte']
        }


class ProjectDomainResource(MyBaseModelResource):
    domain = ForeignKey(AcademicDomainResource, 'domain')
    project = ForeignKey(ProjectResource, 'project')

    class Meta(MyBaseModelResource.Meta):
        resource_name = 'projectdomain'
        queryset = ProjectDomain.objects.all()
        filtering = {
            'project': ALL_WITH_RELATIONS,
            'domain': ALL_WITH_RELATIONS,
            'subdomain':['exact']
        }

