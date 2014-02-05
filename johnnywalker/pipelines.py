# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from scrapy.xlib.pydispatch import dispatcher
from scrapy.exceptions import DropItem
from scrapy.signals import (spider_closed, spider_error)
from . import (MONGO_COLLECTION_LINKS, MONGO_DBNAME)
from stats.miner import mine_data

class SignalProcessor(object):
    def __init__(self):
        pass

    def open_spider(self, spider):
        dispatcher.connect(self.spider_closed_signal, spider_closed)
        dispatcher.connect(self.spider_error_signal, spider_error)

    def spider_closed_signal(self, spider, reason):
        #reason could be in ['finished','cancelled','shutdown']
        mine_data(spider.allowed_domains[0])

    def spider_error_signal(self, spider, failure, response):
        """
        failure - the exception raised as a Twisted Failure object
        response - the response being processed when the exception was raised

        """
        pass

    def process_item(self):
        pass

    def close_spider(self, spider):
        pass


class HashDuplicateFilterPipeline(object):
    def __init__(self):
        self.hashes = []

    def process_item(self, item, spider):
        if item['response_hash'] in self.hashes:
            raise DropItem('duplicate page found')
        self.hashes.append(item['response_hash'])
        return item


class MongoStorePipeline(object):
    def __init__(self):
        self.client = None
        self.link_collection = None

    def open_spider(self, spider):
        self.client = MongoClient()
        db = self.client[MONGO_DBNAME]
        domain = spider.allowed_domains[0]
        collection = db[MONGO_COLLECTION_LINKS][domain]
        if collection.name in db.collection_names():
            db.drop_collection(collection.name)
        self.link_collection = collection

    def process_item(self, item, spider):
        self.link_collection.insert(dict(item))

    def close_spider(self, spider):
        self.client.close()

