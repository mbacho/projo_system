__author__ = 'barbossa'
from scrapy.contrib.spidermiddleware.offsite import OffsiteMiddleware


class MyOffsiteMiddleware(OffsiteMiddleware):
    def __init__(self, *args, **kwargs):
        super(MyOffsiteMiddleware, self).__init__(*args, **kwargs)
