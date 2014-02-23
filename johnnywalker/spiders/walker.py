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


file : walker.py
project : webometrics

"""

from re import sub

from random import randrange
from hashlib import sha256 as sh
from urlparse import (urlsplit, urlunsplit)
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import (CrawlSpider, Rule)
from ..items import WalkerItem
from .. import RICH_FILES
from johnnywalker.models import AvoidUrl


class Walker(CrawlSpider):
    name = 'walker'
    handle_httpstatus_list = [404, 500]
    jobid = None #use with scrapy server
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

    DENY_DOMAINS = ['maktaba.ku.ac.ke', 'opac.mku.ac.ke', 'library.kemu.ac.ke', 'opac.library.strathmore.edu']

    DENY_PATTERNS = [x.url_pattern for x in AvoidUrl.objects.all()]

    rules = (
        Rule(SgmlLinkExtractor(deny_extensions=IGNORED_EXTS, deny=DENY_PATTERNS, deny_domains=DENY_DOMAINS),
             callback='parse_item', follow=True,
             process_request='process_request', process_links='process_links', ),
    )
    start_urls = []
    allowed_domains = []

    def __init__(self, start, domain, _job=None, *args, **kwargs): #_job is given by scrapyd if started by server
        super(Walker, self).__init__(*args, **kwargs)
        if (type(start) is not str) and (type(start) is not unicode):
            raise TypeError('invalid type given for startpage')
        if (type(domain) is not str) and (type(domain) is not unicode):
            raise TypeError('invalid type given for domain')
        if start == '' or domain == '':
            raise ValueError('startpage or domain not provided')

        self.jobid = _job
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
        """called for each list of links extracted from each response using the specified link_extractor."""
        for link in links:
            split_link = urlsplit(link.url)
            link.url = urlunsplit((split_link.scheme, split_link.netloc, sub(r'//+', '/', split_link.path),
                                   split_link.query, split_link.fragment))
        return links

    def process_request(self, request):
        """
        called with every request extracted by this rule, and must return a request or None (to filter out the request)
        """
        ext = request.url.split(".")[-1]
        if ext in RICH_FILES.keys():
            request.method = 'HEAD'
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

    @property
    def collection_name(self):
        """Name to be used to save collection of scraped data"""
        if self.jobid not in [None, '']:
            return self.jobid
        else:
            return self.allowed_domains[0]
