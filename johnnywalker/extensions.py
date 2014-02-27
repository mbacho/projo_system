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


file : extensions.py
project : webometrics

"""
from django.utils.timezone import now
from scrapy.signals import ( spider_closed )
from stats.miner import mine_data
from webui.models import ProjectDomain


class SignalProcessor(object):
    @classmethod
    def from_crawler(cls, crawler):
        # instantiate the extension object
        ext = cls()

        # connect the extension object to signals
        # crawler.signals.connect(ext.spider_opened, signal=spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=spider_closed)
        #crawler.signals.connect(ext.spider_error, signal=spider_error)

        # return the extension object
        return ext

    def spider_opened(self, spider):
        pass

    def spider_closed(self, spider, reason):
        #reason could be in ['finished','cancelled','shutdown']
        if spider.jobid not in (None, ''):
            try:
                pd = ProjectDomain.objects.get(jobid=spider.jobid)
                pd.stoptime = now()
                pd.status = reason
                pd.save()
            except:
                pass

        if reason == 'finished':
            mine_data(spider.collection_name, spider.allowed_domains[0])


    def spider_error(self, spider, failure, response):
        """
        failure - the exception raised as a Twisted Failure object
        response - the response being processed when the exception was raised

        """
        pass


