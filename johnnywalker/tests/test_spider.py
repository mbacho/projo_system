from scrapy.link import Link

from core.tests import TestCase
from core.tests import istest
from ..spiders.walker import Walker


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
            {'good': Link(url='http://localhost')},
            {'bad': Link(url='http://localhost/'), 'good': Link(url='http://localhost/')}
        ]
        res = self.spider.process_links([i['bad'] if i.has_key('bad') else i['good'] for i in links])
        l = len(res)
        for i in range(0, l, 1):
            self.assertEqual(links[i]['good'].url, res[i].url)

    def test_validations(self):
        urls = [
            {'url': 'http://localhost', 'valid': True},
            {'url': 'http://google.com', 'valid': True},
            {'url': 'google.com', 'valid': False},
        ]
        domains = [
            {'domain': 'localhost', 'valid': True},
            {'domain': 'google.com', 'valid': True},
            {'domain': 'sci.uonbi.com', 'valid': True},
        ]
        for i in urls:
            u, ans = i['url'], i['valid']
            res = self.spider.is_valid_url(u)
            self.assertTrue(res == ans, 'url validation error')

        for i in domains:
            d, ans = i['domain'], i['valid']
            res = self.spider.is_valid_domain(d)
            self.assertTrue(res == ans, 'domain validation error')

    def test_rich_files(self):
        self.fail('urgent tests')

    def test_process_request(self):
        pass

    def test_user_agent(self):
        pass

    def test_parse_item(self):
        pass


