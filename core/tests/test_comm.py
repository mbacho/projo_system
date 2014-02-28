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


file : test_comm.py
project : webometrics

"""

from . import TestCase
from core.comm import ScrapydCommunicator


class TestCommunicator(TestCase):
    def setUp(self):
        self.comm = ScrapydCommunicator()

    def test_connection_fail(self):
        self.comm.host = 'hostnotfound'
        ans = self.comm._get_jsondata('notexistent', 'POST', None)
        self.assertEqual(ans['status'], 'error')
        self.comm._get_jsondata('notexistent', 'GET', None)
        self.assertEqual(ans['status'], 'error')

    def test_listprojects(self):
        ans = self.comm.listprojects()
        self.assertEqual(ans['status'], 'ok')
        self.assertIn(self.comm.project, ans['projects'])

    def test_listspiders(self):
        ans = self.comm.listspiders()
        self.assertEqual(ans['status'], 'ok')
        self.assertIn(self.comm.spider, ans['spiders'])

    def test_listjobs(self):
        ans = self.comm.listjobs()
        self.assertEqual(ans['status'], 'ok')
        self.assertIn('pending', ans)
        self.assertIn('running', ans)
        self.assertIn('finished', ans)

    def test_cancel(self):
        ans = self.comm.cancel('somejobid')
        self.assertEqual(ans['status'], 'ok')

    def test_listversions(self):
        ans = self.comm.listversions()
        self.assertEqual(ans['status'], 'ok')

    def test_schedule(self):
        ans = self.comm.schedule('http://somedomain', 'somedomain')
        self.assertEqual(ans['status'], 'ok')
        self.comm.cancel(ans['jobid'])