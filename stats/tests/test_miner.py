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


file : test_miner.py
project : webometrics

"""
from json import loads
from os.path import join, abspath

from pymongo import MongoClient

from core.tests import TestCase,set_trace
from johnnywalker import (MONGO_DBNAME, MONGO_COLLECTION_OUTLINKS, MONGO_COLLECTION_LINKS)
from ..miner import mine_data


class TestMiner(TestCase):
    domain = 'testdomain.com'

    def setUp(self):
        self.client = MongoClient()
        self.db = self.client[MONGO_DBNAME]
        self.links = self.db[MONGO_COLLECTION_LINKS][self.domain]
        self.outlinks = self.db[MONGO_COLLECTION_OUTLINKS][self.domain]
        datadir = abspath(join(__file__, '..'))
        fyl = open(join(datadir, 'data/%s.jsonlines' % self.domain), 'r')
        for i in fyl:
            self.links.insert(loads(i))
        fyl.close()
        fyl = open(join(datadir, 'data/%s.outlinks.jsonlines' % self.domain), 'r')
        for i in fyl:
            self.outlinks.insert(loads(i))
        fyl.close()

    def test_setup(self):
        self.assertEqual(self.links.count(), 10)
        self.assertEqual(self.outlinks.count(), 7)

    def test_mine_data(self):
        stats = mine_data(self.domain)
        self.assertEqual(stats.outlinks, 3)
        self.assertEqual(stats.domain, self.domain)
        self.assertEqual(stats.page_count, 7)
        self.assertEqual(stats.pages_not_found, 3)
        self.assertEqual(stats.richfiles, 2)

    def tearDown(self):
        self.db.drop_collection(self.links.name)
        self.db.drop_collection(self.outlinks.name)
        self.client.close()

