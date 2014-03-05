from django.conf import settings
from pymongo import MongoClient

from scrapy.contrib.spidermiddleware.offsite import OffsiteMiddleware

from ..items import WalkerItem
from johnnywalker.models import RichFile


class MyOffsiteMiddleware(OffsiteMiddleware):
    def __init__(self, *args, **kwargs):
        super(MyOffsiteMiddleware, self).__init__()
        self.client = None
        self.db = None
        self.link_collection = None

    def spider_opened(self, spider):
        super(MyOffsiteMiddleware, self).spider_opened(spider)
        dbname = settings.MONGO_DB['name']
        collection_outlinks = settings.MONGO_DB['outlink_collection']
        self.client = MongoClient()
        self.db = self.client[dbname]
        collection = self.db[collection_outlinks][spider.collection_name]
        if collection.name in self.db.collection_names():
            self.db.drop_collection(collection.name)
        self.link_collection = collection

    def __del__(self):
        if self.client is not None:
            self.client.close()

    def should_follow(self, request, spider):
        ans = super(MyOffsiteMiddleware, self).should_follow(request, spider)
        if not ans:
            lnk = WalkerItem()
            lnk['status'] = ''
            lnk['parent'] = request.headers.get('Referer', '')
            lnk['response_hash'] = ''
            lnk['type'] = ''
            lnk['page'] = request.url
            self.link_collection.insert(dict(lnk))

        return ans
