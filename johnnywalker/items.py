# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class WalkerItem(Item):
    status = Field()
    parent = Field()
    response_hash = Field() #used to identify similar page contents
    type = Field()
    page = Field()

    def __unicode__(self):
        return "{0}, {1}, {2}, {3}".format(self.type, self.status, self.page, self.response_hash)
