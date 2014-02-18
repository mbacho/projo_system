# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from scrapy.exceptions import DropItem
from . import (MONGO_COLLECTION_LINKS, MONGO_DBNAME)


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
        collection = None
        if spider.jobid not in [None, '']:
            collection = db[spider.jobid]
        else:
            domain = spider.allowed_domains[0]
            collection = db[MONGO_COLLECTION_LINKS][domain]
        if collection.name in db.collection_names():
            db.drop_collection(collection.name)
        self.link_collection = collection

    def process_item(self, item, spider):
        self.link_collection.insert(dict(item))

    def close_spider(self, spider):
        self.client.close()

