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


file : test_middleware.py
project : webometrics

"""
from scrapy.http import Request
from core.tests import TestCase
from johnnywalker.spiders.walker import Walker
from ..middleware.offsite import MyOffsiteMiddleware


class TestMyOffsiteMiddleware(TestCase):
    def setUp(self):
        self.middleware = MyOffsiteMiddleware()
        self.spider = Walker('http://startpage', 'domain')

    def test_opened(self):
        self.middleware.spider_opened(self.spider)
        self.assertIsNotNone(self.middleware.client)
        self.assertIsNotNone(self.middleware.db)
        self.assertIsNotNone(self.middleware.link_collection)
        self.assertEqual(self.middleware.host_regex, self.middleware.get_host_regex(self.spider))

    def test_should_follow(self):
        self.middleware.spider_opened(self.spider)
        requests = [
            (Request(url='http://outside'), False),
            (Request(url='http://domain'), True)
        ]
        for i in requests:
            ans = self.middleware.should_follow(i[0], self.spider)
            self.assertEqual(ans, i[1])
