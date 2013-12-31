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

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'johnnywalker (+http://www.yourdomain.com)'
COOKIES_ENABLED = False

from os.path import join, abspath

path = abspath('.')
FEED_URI = join(path, 'data', 'feed_data.jsonlines')
FEED_FORMAT = 'jsonlines'
ROBOTSTXT_OBEY = True
# JOBDIR = 'jobs'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrapytut (the friendly scrapper)'
TELNETCONSOLE_ENABLED = False
WEBSERVICE_ENABLED = True
#WEBSERVICE_RESOURCES = {'scrapytut.webservice.StatsResource':1,'scrapytut.webservice.EngineStatusResource':1,}
#WEBSERVICE_PORT = 8081
#WEBSERVICE_LOGFILE = 'logs/webservice_log'