from os.path import (join, abspath)
from django_nose import FastFixtureTestCase

from scrapy.http import (Response, Request, Headers)
from scrapy.link import Link

from core.tests import istest
from ..spiders.walker import (Walker, sh)


class TestWalker(FastFixtureTestCase):
    fixtures = [
        'johnnywalker/fixtures/initial_data.json'
    ]

    @istest
    def setUp(self):
        with self.assertRaises(TypeError):
            self.spider = Walker(None, '')

        with self.assertRaises(ValueError):
            self.spider = Walker('', '')

        with self.assertRaises(TypeError):
            self.spider = Walker('http://localhost', None)

        self.spider = Walker('http://localhost', 'localhost')
        self.schedule_spider = Walker('http://localhost', 'localhost', 'somejobid')

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

    def test_parse_item(self):
        request_headers = Headers({'referer': 'http://testdomain.com'})
        response_headers = Headers({'content-type': 'text/html'})
        request = Request(url="http://testdomain.com/richfiles", headers=request_headers, body="")
        response = Response(url='http://testdomain.com/richfiles', body=self.get_html('testpage.html'),
                            headers=response_headers,
                            request=request)
        item = self.spider.parse_item(response)
        self.assertEqual(item['page'], 'http://testdomain.com/richfiles')
        self.assertEqual(item['parent'], 'http://testdomain.com')
        self.assertEqual(item['response_hash'], sh(self.get_html('testpage.html')).hexdigest())

    def test_process_request(self):
        exts = {
            '.html': 'get',
            '.doc': 'head',
            '.pdf': 'head',
            '': 'get'
        }
        base_url = 'http://testdomain.com/page'

        for k in exts:
            req = Request(url=base_url + k, method='get')
            ans = self.spider.process_request(req)
            self.assertEqual(ans.method.lower(), exts[k], "%s ==> %s" % (req.url, ans.method))

    def test_linkextractions(self):
        links = [
            {'good': 'http://testdomain.com'},
            {'good': 'http://testdomain.com/gp', 'bad': 'http://testdomain.com///gp'},
        ]
        for i in links:
            bad = Link(i['bad']) if 'bad' in i.keys() else Link(i['good'])
            ans = self.spider.process_links([bad])[0]
            self.assertEqual(ans.url, i['good'])

    def test_spiderrules(self):
        self.skipTest('test spider rules, denydomains, denyurls e.t.c.')

    def test_collection_name(self):
        self.assertEqual(self.spider.collection_name, 'localhost')
        self.assertEqual(self.schedule_spider.collection_name, 'somejobid')

    def get_html(self, filename):
        fpath = abspath(join(__file__, '..'))
        f = open(join(fpath, 'html/%s' % filename), 'r')
        s = f.read()
        f.close()
        return s
