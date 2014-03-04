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


file : website.py
project : webometrics

"""

from datetime import datetime
from os.path import abspath, join

import django
from django.template.loader import render_to_string
import rest_framework
from twisted.web import resource, static
from twisted.application.service import IServiceCollection
from scrapy.utils.misc import load_object
from scrapyd.interfaces import IPoller, IEggStorage, ISpiderScheduler


class Root(resource.Resource):
    def __init__(self, config, app, wsgi_resource):
        resource.Resource.__init__(self)
        self.debug = config.getboolean('debug', False)
        self.runner = config.get('runner')
        self.app = app
        services = config.items('services', ())
        for servName, servClsName in services:
            servCls = load_object(servClsName)
            self.putChild(servName, servCls(self))
        self.update_projects()
        self.wsgi_resource = wsgi_resource

    def getChild(self, path, request):
        path0 = request.prepath.pop(0)
        request.postpath.insert(0, path0)
        return self.wsgi_resource

    def update_projects(self):
        self.poller.update_projects()
        self.scheduler.update_projects()

    @property
    def launcher(self):
        app = IServiceCollection(self.app, self.app)
        return app.getServiceNamed('launcher')

    @property
    def scheduler(self):
        return self.app.getComponent(ISpiderScheduler)

    @property
    def eggstorage(self):
        return self.app.getComponent(IEggStorage)

    @property
    def poller(self):
        return self.app.getComponent(IPoller)

    def get_log_url(self, jobid):
        return "/static/items/johnnywalker/walker/{0}.log".format(jobid)

    def get_items_url(self, jobid):
        return "/static/items/johnnywalker/walker/{0}.jl".format(jobid)


class CrawlerStats(resource.Resource):
    def __init__(self, root):
        resource.Resource.__init__(self)
        self.root = root

    def render(self, txrequest):
        # from nose.tools import set_trace
        # set_trace()
        queue_list = self.root.poller.queues.items()[0]
        queue_list = queue_list[1].list()
        pending = [{
                       'name': i['name'],
                       'job': i['_job']
                   } for i in queue_list]
        running = [{
                       'job': i['job'],
                       'pid': i['pid'],
                       'runtime': datetime.now() - i['start_time'],
                       'log_url': self.root.get_log_url(i['job']),
                       'items_url': self.root.get_items_url(i['job'])
                   } for i in self.root.launcher.processes.values()]
        finished = [{
                        'job': i['job'],
                        'runtime': i['end_time'] - i['start_time'],
                        'log_url': self.root.get_log_url(i['job']),
                        'items_url': self.root.get_items_url(i['job'])
                    } for i in self.root.launcher.finished]
        data = {
            'pending': pending,
            'running': running,
            'finished': finished
        }

        return bytes(render_to_string('johnnywalker/home.html', data))


class StaticFile(static.File):
    def __init__(self):
        super(StaticFile, self).__init__(join(abspath("."), "static"))
        self.staticadminsrc = static.File(join(django.__path__[0], "contrib/admin/static"))
        self.staticrestsrc = static.File(join(rest_framework.__path__[0], "static"))

    def getChild(self, path, request):
        if path == 'admin':
            return self.staticadminsrc.getChild(path, request)
        elif path == 'rest_framework':
            return self.staticrestsrc.getChild(path, request)

        return super(StaticFile, self).getChild(path, request)

