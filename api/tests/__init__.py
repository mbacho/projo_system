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


file : __init__.py.py
project : webometrics

"""
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase


class TestAPI(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url_name = ''
        user, username, email, password = \
            None, 'testuser', 'testmail@mail.com', 'pass'
        user = User.objects.get_or_create(username=username, email=email, password=password)
        self.user = user[0]

    def auth_client(self):
        self.client.force_authenticate(user=self.user)

    def tearDown(self):
        self.user.delete()

    @property
    def list_url(self):
        return self.url_name + '-list'

    @property
    def detail_url(self):
        return self.url_name + '-detail'
