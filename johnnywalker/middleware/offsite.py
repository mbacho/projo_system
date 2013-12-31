__author__ = 'barbossa'
from johnnywalker.items import WalkerItem
from scrapy.contrib.spidermiddleware.offsite import OffsiteMiddleware


class MyOffsiteMiddleware(OffsiteMiddleware):
    def __init__(self, *args, **kwargs):
        super(MyOffsiteMiddleware, self).__init__()

    def should_follow(self, request, spider):
        ans = super(MyOffsiteMiddleware, self).should_follow(request, spider)
        if not ans:
            lnk = WalkerItem()
            lnk['status'] = ''
            lnk['parent'] = request.headers.get('Referer', '')
            lnk['response_hash'] = ''
            lnk['type'] = ''
            lnk['page'] = request.url
        return ans
