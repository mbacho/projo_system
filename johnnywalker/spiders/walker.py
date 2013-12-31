from random import randrange

from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule


__author__ = 'barbossa'


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
        'css', 'exe', 'bat', 'bin', 'rss', 'zip', 'rar', 'xml'
    ]

    rules = (
        Rule(SgmlLinkExtractor(deny_extensions=IGNORED_EXTS), callback='parse_item', follow=True,
             process_links='process_links', process_request='process_request'),
    )

    def __init__(self, startpage, domain, *args, **kwargs):
        super(Walker, self).__init__(args, kwargs)
        self.start_urls = [startpage]
        self.allowed_domains = [domain]


    def parse_item(self, response):
        pass

    def process_results(self, response, results):
        """
        This method is called for each result (item or request) returned by the spider, and it's intended to perform
        any last time processing required before returning the results to the framework core, for example setting
        the item IDs. It receives a list of results and the response which originated those results. It must return a
        list of results (Items or Requests).
        """
        pass

    def process_links(self, links):
        """
        called for each list of links extracted from each response using the specified link_extractor.
        """
        return links

    def process_request(self, request):
        """
        called with every request extracted by this rule, and must return a request or None (to filter out the request)
        """
        pass

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
