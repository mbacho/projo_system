# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from django.conf import settings

from pymongo import MongoClient
from scrapy.exceptions import DropItem


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
        dbname = settings.MONGO_DB['name']
        collection_links = settings.MONGO_DB['link_collection']

        db = self.client[dbname]
        collection = db[collection_links][spider.collection_name]
        if collection.name in db.collection_names():
            db.drop_collection(collection.name)
        self.link_collection = collection

    def process_item(self, item, spider):
        self.link_collection.insert(dict(item))

    def close_spider(self, spider):
        self.client.close()

