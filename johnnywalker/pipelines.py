# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from os.path import join, abspath
from json import dump

from scrapy.exceptions import DropItem


class JsonLinesDomainPipeline(object):
    def __init__(self):
        self.file = None


    def process_item(self, item, spider):
        dump(dict(item), self.file)
        return item


    def open_spider(self, spider):
        domain = spider.allowed_domains[0]
        path = abspath(join(__file__, '..'))
        fname = join(path, 'data', "%s.jsonlines" % domain)
        self.file = open(fname, 'w')


    def close_spider(self, spider):
        if self.file is not None:
            if not self.file.closed:
                self.file.close()


class HashDuplicateFilterPipeline(object):
    def __init__(self):
        self.hashes = []

    def process_item(self, item, spider):
        if item['response_hash'] in self.hashes:
            raise DropItem('duplicate page found')
        self.hashes.append(item['response_hash'])
        return item

