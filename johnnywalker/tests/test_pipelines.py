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


file : test_pipelines.py
project : webometrics

"""
from json import (dumps, loads)
from os import remove

from scrapy.exceptions import DropItem

from core.tests import TestCase
from core.tests import istest
from johnnywalker.items import WalkerItem
from johnnywalker.pipelines import (JsonLinesDomainPipeline, HashDuplicateFilterPipeline)
from johnnywalker.spiders.walker import Walker


class TestJsonLinesDomainPipeline(TestCase):
    @istest
    def setUp(self):
        self.pipeline = JsonLinesDomainPipeline()
        self.spider = Walker(domain='testdomain.com', start='http://testdomain.com')
        self.pipeline.open_spider(self.spider)
        self.assertIsNotNone(self.pipeline.file)

    def test_process_item(self):
        item = WalkerItem()
        item['response_hash'] = '3829rerw98'
        item['page'] = 'http://testdomain.com/home'
        item['parent'] = 'http://testdomain.com/'
        item['status'] = 200
        item['type'] = 'text/html'
        self.pipeline.process_item(item, self.spider)
        fname = self.pipeline.file.name
        f = open(fname, 'r')
        lines = f.readlines()
        f.close()
        self.assertEqual(loads(lines[-1]), loads(dumps(dict(item))))

    def test_close_spider(self):
        self.pipeline.close_spider(self.spider)
        self.assertTrue(self.pipeline.file.closed)
        #TODO : Why ain't the remove working?
        remove(self.pipeline.file.name)


class TestHashDuplicateFilterPipeline(TestCase):
    def setUp(self):
        self.pipeline = HashDuplicateFilterPipeline()
        self.spider = Walker(domain='testdomain.com', start='http://testdomain.com')

    def test_process_item(self):
        item = WalkerItem()
        item['response_hash'] = '0324u24'
        self.pipeline.process_item(item, self.spider)
        self.assertEqual(len(self.pipeline.hashes), 1)

        with self.assertRaises(DropItem):
            self.pipeline.process_item(item, self.spider)

