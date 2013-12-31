from unittest import TestCase
from unittest import SkipTest
from nose.tools import istest
from johnnywalker.spiders.walker import Walker

__author__ = 'barbossa'


class TestWalker(TestCase):
    @istest
    def setUp(self):
        with self.assertRaises(TypeError):
            self.spider = Walker(None, '')

        with self.assertRaises(ValueError):
            self.spider = Walker('', '')

        self.spider = Walker('http://localhost', 'localhost')

    def test_urls(self):
        self.assertEqual(len(self.spider.start_urls), 1)
        self.assertEqual(len(self.spider.allowed_domains), 1)

    def test_process_links(self):
        links = [
            {'good': 'http://localhost'},
            {'bad': 'http://localhost/', 'good': 'http://localhost/'}
        ]
        for i in links:
            poa, mbaya = i['good'], (i['bad'] if i.has_key('bad') else i['good'])
            res = self.spider.process_links(mbaya)
            self.assertEqual(poa, res)


    def test_process_request(self):
        pass

    def test_user_agent(self):
        raise SkipTest()

    def test_parse_item(self):
        pass

