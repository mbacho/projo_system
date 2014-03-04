"""
The MIT License

Copyright (c) 2014, mbacho (Chomba Ng'ang'a)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.


file : app.py
project : webometrics

"""

import os
from scrapy.utils.misc import load_object
from scrapyd import Config
from scrapyd.eggstorage import FilesystemEggStorage
from scrapyd.environ import Environment
from scrapyd.interfaces import IPoller, IEggStorage, ISpiderScheduler, IEnvironment
from scrapyd.poller import QueuePoller
from scrapyd.scheduler import SpiderScheduler

from twisted.application import internet, service
from twisted.application.internet import TimerService
from twisted.web import server, wsgi
from twisted.python import threadpool
from twisted.internet import reactor

from combi_server.twresource import CrawlerStats, Root, StaticFile

PORT = 8000


class ThreadPoolService(service.Service):
    def __init__(self, pool):
        self.pool = pool

    def startService(self):
        service.Service.startService(self)
        self.pool.start()

    def stopService(self):
        service.Service.stopService(self)
        self.pool.stop()

# Environment setup for your Django project files:
os.environ['DJANGO_SETTINGS_MODULE'] = 'webometrics.settings.develop'
from django.core.handlers.wsgi import WSGIHandler

# Twisted Application Framework setup:
application = service.Application('twisted-django')


#scrapyd setup
config = Config()
poll_interval = config.getfloat('poll_interval', 10)
poller = QueuePoller(config)
eggstorage = FilesystemEggStorage(config)
scheduler = SpiderScheduler(config)
environment = Environment(config)
application.setComponent(IPoller, poller)
application.setComponent(IEggStorage, eggstorage)
application.setComponent(ISpiderScheduler, scheduler)
application.setComponent(IEnvironment, environment)
laupath = config.get('launcher', 'scrapyd.launcher.Launcher')
laucls = load_object(laupath)
launcher = laucls(config, application)
timer = TimerService(poll_interval, poller.poll)
launcher.setServiceParent(application)
timer.setServiceParent(application)


# WSGI container for Django, combine it with twisted.web.Resource:
# XXX this is the only 'ugly' part: see the 'getChild' method in twresource.Root
# The MultiService allows to start Django and Twisted server as a daemon.

multi = service.MultiService()
pool = threadpool.ThreadPool()
tps = ThreadPoolService(pool)
tps.setServiceParent(multi)
webresource = wsgi.WSGIResource(reactor, tps.pool, WSGIHandler())
#root = Root(webresource)
root = Root(config, application, webresource)

# Servce Django media files off of /media:
# mediasrc = static.File(os.path.join(os.path.abspath("."), "mydjangosite/media"))

staticsrc = StaticFile()
# root.putChild("media", mediasrc)
root.putChild("static", staticsrc)

root.putChild('crawler_stats', CrawlerStats(root))

# Serve it up:
main_site = server.Site(root)
internet.TCPServer(PORT, main_site).setServiceParent(multi)
multi.setServiceParent(application)

