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

from core.tests import TestCase
from crawler_server.tasks import debug_task, DebugTask, RunSpiderTask


class TestCrawlerServer(TestCase):
    def test_jobs(self):
        a = debug_task.delay()
        self.assertEqual(a.get(), 'debug_task')
        self.assertTrue(a.successful())

        rst = DebugTask()
        a = rst.delay()
        self.assertEqual(a.get(), 'debug_class')
        self.assertTrue(a.successful())


class TestRunSpiderTask(TestCase):
    def setUp(self):
        self.rst = RunSpiderTask()

    def test_run(self):
        self.rst.run('localhost', 'http://localhost')

    def test_delay(self):
        self.rst.delay(domain='localhost', starturl='http://localhost')

    def tearDown(self):
        pass
