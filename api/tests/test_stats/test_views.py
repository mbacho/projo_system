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
from django.core.urlresolvers import reverse
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_200_OK
from api.tests import TestAPI


class TestDomainStatsViewSet(TestAPI):
    def setUp(self):
        super(TestDomainStatsViewSet, self).setUp()
        self.url_name = 'domainstats'

    def test_unauth(self):
        response = self.client.get(reverse(self.list_url))
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_auth(self):
        self.auth_client()
        response = self.client.get(reverse(self.list_url))
        self.assertEqual(response.status_code, HTTP_200_OK)

