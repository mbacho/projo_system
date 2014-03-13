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
from os.path import (join, abspath, dirname)

from pymongo import MongoClient
from django.conf import settings

from core.tests import TestCase
from johnnywalker.models import RichFile
from ..miner import Miner, HistoryMiner
from ..tasks import MinerTask, HistoryMinerTask
from webui.models import ProjectDomain


class TestMiner(TestCase):
    fixtures = [
        'johnnywalker/fixtures/initial_data.json',
        'tests/domainstats.json'
    ]

    def setUp(self):
        dbname = settings.MONGO_DB['name']
        collection_links = settings.MONGO_DB['link_collection']
        collection_outlinks = settings.MONGO_DB['outlink_collection']
        rich_files = [x.ext for x in RichFile.objects.all()]

        self.project_domain = ProjectDomain.objects.get(id=1)
        self.client = MongoClient()
        self.db = self.client[dbname]
        self.links = self.db[collection_links][self.project_domain.domain.domain]
        self.outlinks = self.db[collection_outlinks][self.project_domain.domain.domain]
        datadir = abspath(join(dirname(__file__), 'data'))
        fyl = open(join(datadir, '%s.links.jsonlines' % self.project_domain.domain.domain), 'r')
        for i in fyl:
            self.links.insert(loads(i))
        fyl.close()
        fyl = open(join(datadir, '%s.outlinks.jsonlines' % self.project_domain.domain.domain), 'r')
        for i in fyl:
            self.outlinks.insert(loads(i))
        fyl.close()
        self.miner = Miner(self.project_domain.domain.domain, self.project_domain)

    def test_setup(self):
        self.assertEqual(self.links.count(), 10)
        self.assertEqual(self.outlinks.count(), 7)
        self.assertIsNotNone(self.miner)

    def test_webometric(self):
        with self.assertRaises(ValueError):
            miner = Miner('somedomain.co.ke', 'somedomain.co.ke')
        stats = self.miner.webometric()
        self.assertIsNotNone(stats.projectdomain)
        self.assertEqual(stats.outlinks, 3)
        self.assertEqual(stats.projectdomain, self.project_domain)
        self.assertEqual(stats.page_count, 7)
        self.assertEqual(stats.pages_not_found, 3)
        self.assertEqual(stats.richfiles, 2)

    def test_pagerank(self):
        pr = self.miner.pagerank()
        self.assertIsNotNone(pr)

    def test_miner_task(self):
        miner_task = MinerTask()
        async = miner_task.delay(self.project_domain.domain.domain, self.project_domain)
        self.assertTrue(async.successful())

    def tearDown(self):
        self.db.drop_collection(self.links.name)
        self.db.drop_collection(self.outlinks.name)
        self.client.close()


class TestHistory(TestCase):
    fixtures = [
        'johnnywalker/fixtures/initial_data.json',
        'tests/domainstats.json'
    ]

    def setUp(self):
        self.project_domain = ProjectDomain.objects.get(id=1)
        self.hist_miner = HistoryMiner(self.project_domain)

    def test_history_miner(self):
        ans = self.hist_miner.get_history()
        self.assertGreaterEqual(len(ans), 1)

    def test_task(self):
        miner_task = HistoryMinerTask()
        async = miner_task.delay(self.project_domain)
        self.assertTrue(async.successful())