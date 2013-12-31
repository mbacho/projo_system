
__author__ = 'barbossa'

from random import randrange
from hashlib import sha256 as sh
from urlparse import urlsplit

from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from johnnywalker.items import WalkerItem


class Walker(CrawlSpider):
    name = 'walker'
    handle_httpstatus_list = [404]
    IGNORED_EXTS = [
        # images
        'mng', 'pct', 'bmp', 'gif', 'jpg', 'jpeg', 'png', 'pst', 'psp', 'tif',
        'tiff', 'ai', 'drw', 'dxf', 'eps', 'svg',

        # audio
        'mp3', 'wma', 'ogg', 'wav', 'ra', 'aac', 'mid', 'au', 'aiff',

        # video
        '3gp', 'asf', 'asx', 'avi', 'mov', 'mp4', 'mpg', 'qt', 'rm', 'swf', 'wmv', 'm4a', 'mpeg',

        # other
        'css', 'exe', 'bat', 'bin', 'rss', 'zip', 'rar', 'xml',

        #script files
        'js', 'css', 'vbs', 'cs',
    ]

    rules = (
        Rule(SgmlLinkExtractor(deny_extensions=IGNORED_EXTS), callback='parse_item', follow=True,
             process_links='process_links', process_request='process_request'),
    )
    start_urls = []
    allowed_domains = []

    def __init__(self, start, domain, *args, **kwargs):
        super(Walker, self).__init__(*args, **kwargs)
        if type(start) is not str or type(domain) is not str:
            raise TypeError('invalid type given for startpage or domain')
        if start == '' or domain == '':
            raise ValueError('startpage or domain not provided')

        self.start_urls = [start]
        self.allowed_domains = [domain]


    def parse_item(self, response):
        lnk = WalkerItem()
        lnk['status'] = response.status
        lnk['parent'] = response.request.headers.get('Referer', '')
        lnk['response_hash'] = '' if response.status != 200 else sh(response.body).hexdigest()

        type = response.headers['Content-Type']
        if ';' in type:
            type = type[:type.index(';')]
        lnk['type'] = type
        lnk['page'] = response.url
        return lnk

    def process_results(self, response, results):
        """
        This method is called for each result (item or request) returned by the spider, and it's intended to perform
        any last time processing required before returning the results to the framework core, for example setting
        the item IDs. It receives a list of results and the response which originated those results. It must return a
        list of results (Items or Requests).
        """
        return results

    def process_links(self, links):
        """
        called for each list of links extracted from each response using the specified link_extractor.
        """
        processed_links = []
        for i in links:
            split_link = urlsplit(i.url)
            if split_link.netloc in self.allowed_domains:
                processed_links.append(i)
            else:
                pass
        return processed_links

    def process_request(self, request):
        """
        called with every request extracted by this rule, and must return a request or None (to filter out the request)
        """
        return request

    def is_valid_domain(self, domain):
        if domain != '':
            return True

        return False

    def is_valid_url(self, url):
        split_url = urlsplit(url)
        if split_url.scheme != '' and split_url.netloc:
            return True
        return False

    @property
    def user_agent(self):
        agents = [
            "chrome",
            "firefox",
            "opera",
            "safari",
        ]
        rand = randrange(0, len(agents))
        return agents[rand]
