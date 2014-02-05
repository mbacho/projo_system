# Scrapy settings for johnnywalker project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'johnnywalker'

SPIDER_MODULES = ['johnnywalker.spiders']
NEWSPIDER_MODULE = 'johnnywalker.spiders'
COOKIES_ENABLED = False
ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'johnnywalker.pipelines.HashDuplicateFilterPipeline':10,
    'johnnywalker.pipelines.MongoStorePipeline': 20,
    #'johnnywalker.pipelines.JsonLinesDomainPipeline': 30
}

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.defaultheaders.DefaultHeadersMiddleware': None,
    'johnnywalker.middleware.downloader.MyHeadersMiddleware': 550,
}

SPIDER_MIDDLEWARES = {
    'scrapy.contrib.spidermiddleware.offsite.OffsiteMiddleware': None,
    'johnnywalker.middleware.offsite.MyOffsiteMiddleware': 500
}


#from os.path import join, abspath
#path = abspath('.')
#FEED_URI = join(path, 'data', 'feed_data.jsonlines')
#FEED_FORMAT = 'jsonlines'

JOBS_TOPDIR = 'jobs'

TELNETCONSOLE_ENABLED = False
WEBSERVICE_ENABLED = True
#WEBSERVICE_RESOURCES = {'scrapytut.webservice.StatsResource':1,'scrapytut.webservice.EngineStatusResource':1,}
#WEBSERVICE_PORT = 8081
#WEBSERVICE_LOGFILE = 'logs/webservice_log'
