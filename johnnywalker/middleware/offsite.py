from os.path import join, abspath
from json import dump

__author__ = 'mbacho'
from ..items import WalkerItem
from scrapy.contrib.spidermiddleware.offsite import OffsiteMiddleware


class MyOffsiteMiddleware(OffsiteMiddleware):
    def __init__(self, *args, **kwargs):
        super(MyOffsiteMiddleware, self).__init__()
        self.file = None

    def spider_opened(self, spider):
        super(MyOffsiteMiddleware, self).spider_opened(spider)
        domain = spider.allowed_domains[0]
        path = abspath(join(__file__, '..', '..'))
        fname = join(path, 'data', "%s.outlinks.jsonlines" % domain)
        self.file = open(fname, 'w')


    def __del__(self):
        if self.file is not None:
            if not self.file.closed:
                self.file.close()

    def should_follow(self, request, spider):
        ans = super(MyOffsiteMiddleware, self).should_follow(request, spider)
        if not ans:
            lnk = WalkerItem()
            lnk['status'] = ''
            lnk['parent'] = request.headers.get('Referer', '')
            lnk['response_hash'] = ''
            lnk['type'] = ''
            lnk['page'] = request.url
            dump(dict(lnk), self.file)
            self.file.write("\n")
            self.file.flush()

        return ans
