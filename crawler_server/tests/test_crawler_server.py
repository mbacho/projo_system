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


file : test_crawler_server.py
project : webometrics

"""
from celery.exceptions import TaskRevokedError

from core.tests import TestCase
from crawler_server.tasks import debug_task, DebugTask, RunSpider, CancelSpider


class TestCrawlerServer(TestCase):
    def test_jobs(self):
        a = debug_task.delay()
        self.assertEqual(a.get(), 'debug_task')
        self.assertTrue(a.successful())

        rst = DebugTask()
        a = rst.delay()
        self.assertEqual(a.get(), 'debug_class')
        self.assertTrue(a.successful())


class TestSpiderTasks(TestCase):
    def setUp(self):
        self.rs = RunSpider()
        self.cs = CancelSpider()

    def test_run_spider(self):
        a = self.rs.delay(domain='localhost', starturl='http://localhost')
        self.assertTrue(a.successful())
        # jobdir = settings.CRAWLER_DIRS['jobdir']
        # logdir = settings.CRAWLER_DIRS['logdir']
        # self.assertTrue(exists(join(jobdir, a.task_id)))
        # self.assertTrue(exists(join(logdir, a.task_id)))

    def test_spider_cancel(self):
        a = self.cs.delay('some-random-test-task-id')
        self.assertIsNotNone(a)
        #self.assertIsInstance(a.info, TaskRevokedError)
        self.assertTrue(a.successful())

    def tearDown(self):
        pass

