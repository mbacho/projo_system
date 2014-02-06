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

from scrapy.exceptions import DropItem

from core.tests import TestCase
from johnnywalker import MONGO_DBNAME
from johnnywalker.items import WalkerItem
from johnnywalker.pipelines import (MongoStorePipeline, HashDuplicateFilterPipeline)
from johnnywalker.spiders.walker import Walker


class TestMongoStorePipeline(TestCase):
    domain = 'testdomain.com'

    def setUp(self):
        self.pipeline = MongoStorePipeline()
        self.spider = Walker(domain='testdomain.com', start='http://testdomain.com')

    def test_open_spider(self):
        self.pipeline.open_spider(self.spider)
        self.client = self.pipeline.client
        self.assertIsNotNone(self.client)
        self.db = self.client[MONGO_DBNAME]
        self.assertIsNotNone(self.db)
        self.links = self.pipeline.link_collection

    def test_process_item(self):
        item = WalkerItem()
        item['response_hash'] = '8ewr98'
        item['type'] = 'text/html'
        item['parent'] = 'http://testdomain.com'
        item['page'] = 'http://testdomain.com/about'
        self.pipeline.process_item(item, self.spider)
        self.assertEqual(self.links.count(), 1)

    def test_close_spider(self):
        self.pipeline.close_spider(self.spider)

    def tearDown(self):
        self.db.drop_collection(self.links.name)


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

