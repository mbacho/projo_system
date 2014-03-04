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
from scrapy.signals import ( spider_closed, spider_error)
from stats.miner import mine_data
from webui.models import ProjectDomain


class SignalProcessor(object):
    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        crawler.signals.connect(ext.spider_closed, signal=spider_closed)
        crawler.signals.error(ext.spider_error, signal=spider_error)
        return ext

    def spider_closed(self, spider, reason):
        """
        reason could be:
        finished: closed because the spider has completed scraping
        cancelled: spider was manually closed
        shutdown: engine was shutdown (for example, by hitting Ctrl-C to stop it)
        """
        pd = None
        if spider.jobid not in [None, '']:
            try:
                pd = ProjectDomain.objects.get(jobid=spider.jobid)
                pd.stoptime = now()
                pd.status = reason
                pd.save()
            except:
                pass

        if reason == 'finished':
            mine_data(spider.collection_name, pd)
        elif reason == 'cancelled':
            pass
        elif reason == 'shutdown':
            pass

    def spider_error(self, failure, response, spider):
        pass
