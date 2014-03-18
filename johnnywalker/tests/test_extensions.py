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


file : test_extenstions.py
project : webometrics

"""
from django.contrib.auth.models import User

from scrapy.crawler import Crawler
from scrapy.settings import Settings

from core.tests import (TestCase )
from ..extensions import SignalProcessor
from johnnywalker.models import AcademicDomain
from johnnywalker.spiders.walker import Walker
from webui.models import ProjectDomain, Project


class TestSignalProcessor(TestCase):
    fixtures = ['test_extensions.json']

    def setUp(self):
        self.crawler = Crawler(Settings())
        self.extension = SignalProcessor()
        self.spider = Walker(start='http://testdomain.com', domain='localhost', _job='somejobid')
        user = User.objects.create_user('testyusa', 'test@mail.com', 'pass')
        project = Project()
        project.owner = user
        project.name = 'testdomain'
        project.save()
        domain = AcademicDomain()
        domain.name = 'testdomain'
        domain.domain = 'testdomain.com'
        domain.link = 'http://testdomain.com'
        domain.save()
        projectdomain = ProjectDomain()
        projectdomain.jobid = 'somejobid'
        projectdomain.domain = domain
        projectdomain.project = project
        projectdomain.save()
        self.spider.set_crawler(self.crawler)

    def test_setUp(self):
        self.assertIsNotNone(self.extension)

    def test_spider_closed(self):
        self.extension.spider_closed(self.spider, 'shutdown')
        projectdomain = ProjectDomain.objects.get(jobid='somejobid')
        self.assertEqual(projectdomain.status, 'shutdown')

    def test_from_crawler(self):
        ext = SignalProcessor.from_crawler(self.crawler)
