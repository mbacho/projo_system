# Create your views here.
from json import loads
from urllib2 import urlopen
from urlparse import urljoin

from django.http import HttpResponse

from django.shortcuts import render_to_response
from django.template import RequestContext
from scrapy.utils.jsonrpc import jsonrpc_client_call
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import signals
from scrapy.utils.project import get_project_settings

from johnnywalker.forms import StartCrawlForm

from .spiders.walker import Walker

from scrapy import log

class ScrapydCommunicator(object):
    host = 'localhost'
    port = 6080
    spidername = 'walker'

    def __init__(self):
        pass

    def start_spider(self, startpage, domain):
        """start <spider> - start/resume spider"""
        return self.jsonrpc_call('crawler/engine', 'open_spider', self.spidername, start=startpage, domain=domain)

    def pause_spider(self):
        """stop <spider> - stop a running spider"""
        return self.jsonrpc_call('crawler/engine', 'close_spider', self.spidername)

    def stop_spider(self):
        pass

    def active_spiders(self):
        return self.json_get('crawler/engine/open_spiders')

    def jsonrpc_call(self, path, method, *args, **kwargs):
        url = self.get_wsurl(path)
        result = jsonrpc_client_call(url, method, *args, **kwargs)
        return result

    def get_wsurl(self, path):
        return urljoin("http://%s:%s/" % (self.host, self.port), path)

    def json_get(self, path):
        url = self.get_wsurl(path)
        return loads(urlopen(url).read())


def create_spider(startpage, domain):
    spider = Walker(startpage, domain)
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    log.start()
    reactor.run()
    return spider


def home(request):
    frm = StartCrawlForm(request.POST or None)
    if frm.is_valid():
        startpage, domain = frm.cleaned_data['startpage'], frm.cleaned_data['domain']
        comms = ScrapydCommunicator()
        # ans = comms.start_spider(domain=domain, startpage=startpage)
        # return HttpResponse(content=ans.__str__())
        spider = create_spider(startpage, domain)
        import pdb;pdb.set_trace()
        active = comms.active_spiders()
        return render_to_response('johnnywalker/home.html', {'active_spiders': active})

    return render_to_response('johnnywalker/home.html', {'startcrawlform': frm},
                              context_instance=RequestContext(request))


def start(request):
    return HttpResponse('spider started')


def pause(request):
    pass


