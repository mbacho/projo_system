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


file : test_api.py
project : webometrics

"""
from django.contrib.auth.models import User
from tastypie.test import ResourceTestCase
from ..api import (ProjectResource, AcademicDomainResource, ProjectDomainResource, UserResource)


class MyBaseResourceTestCase(ResourceTestCase):
    apitest = None

    def setUp(self):
        super(MyBaseResourceTestCase, self).setUp()
        # Create a user.
        self.username = 'yusa'
        self.password = 'pass'
        self.email = 'yusa@mail.com'
        self.user = User.objects.create_user(self.username, self.email, self.password)

    def get_credentials(self):
        return self.create_basic(self.username, self.password)


class TestUserResource(MyBaseResourceTestCase):
    def setUp(self):
        super(TestUserResource, self).setUp()
        self.apitest = UserResource()

    def test_get_unauthorzied(self):
        self.assertHttpUnauthorized(self.api_client.get('/api/user/'))

    def test_resource_ok(self):
        self.assertHttpOK(self.api_client.get('/api/user/', authentication=self.get_credentials()))

class TestProjectResource(MyBaseResourceTestCase):
    def setUp(self):
        super(TestProjectResource, self).setUp()
        self.apitest = ProjectResource()

    def test_get_unauthorzied(self):
        self.assertHttpUnauthorized(self.api_client.get('/api/project/'))

    def test_resource_ok(self):
        self.assertHttpOK(self.api_client.get('/api/project/', authentication=self.get_credentials()))

class TestAcademicDomainResource(MyBaseResourceTestCase):
    def setUp(self):
        super(TestAcademicDomainResource, self).setUp()
        self.apitest = AcademicDomainResource()

    def test_get_unauthorzied(self):
        self.assertHttpUnauthorized(self.api_client.get('/api/domain/'))

    def test_resource_ok(self):
        self.assertHttpOK(self.api_client.get('/api/domain/', authentication=self.get_credentials()))

class TestProjectDomainResource(MyBaseResourceTestCase):
    def setUp(self):
        super(TestProjectDomainResource, self).setUp()
        self.apitest = ProjectDomainResource()

    def test_get_unauthorzied(self):
        self.assertHttpUnauthorized(self.api_client.get('/api/projectdomain/'))

    def test_resource_ok(self):
        self.assertHttpOK(self.api_client.get('/api/projectdomain/', authentication=self.get_credentials()))

