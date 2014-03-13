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


file : test_views.py
project : webometrics

"""
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django.test import TestCase, Client


class TestWebuiViews(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        user = User.objects.get_or_create(username='testuser', email='testmail@mail.com', password='pass')
        self.user = user[0]

    def test_home(self):
        response = self.client.get('/', follow=True)
        self.assertIn(reverse('signin'), response.request['PATH_INFO'])

        self.client.login(username=self.user.username, password=self.user.password)
        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, 200)
        # context_list = response.context
        # context = context_list[-1]
        # self.assertIn('projects', context, 'projects not found')
        self.client.logout()

    def test_signup(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_signin(self):
        response = self.client.get(reverse('signin'))
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_signout(self):
        response = self.client.get(reverse('signout'), follow=True)
        self.assertIn(reverse('signin'), response.request['PATH_INFO'])
        self.assertEqual(response.status_code, 200)

    def test_results(self):
        response = self.client.get(reverse('results'), follow=True)
        self.assertIn(reverse('signin'), response.request['PATH_INFO'])
        self.client.login(username=self.user.username, password=self.user.password)
        self.assertEqual(response.status_code, 200)
        self.client.logout()
