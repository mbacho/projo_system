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


file : views.py
project : webometrics

"""


from time import time
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from kombu.five import monotonic

from celery.task.control import inspect


@login_required
def home(request):
    # {u'celery@blackpearl': [
    #     {
    #         u'args': u'[]',
    #         u'time_start': 37030.852239337,
    #         u'name': u'crawler_server.tasks.RunSpider',
    #         u'delivery_info': {
    #             u'priority': None,
    #             u'redelivered': False,
    #             u'routing_key': u'celery',
    #             u'exchange': u'celery'
    #         },
    #         u'hostname': u'celery@blackpearl',
    #         u'acknowledged': True,
    #         u'kwargs': u"{u'domain': u'localhost', u'starturl': u'http://localhost/bizlist/'}",
    #         u'id': u'a5fcab29-376a-4cfe-9281-746e99bb100d',
    #         u'worker_pid': 23993
    #     }
    # ]
    # }
    i = inspect()
    raw_active = i.active().values()[0]
    active = [{
                  'id': act['id'],
                  'pid': act['worker_pid'],
                  'start_time': datetime.fromtimestamp(time() - (monotonic() - act['time_start'])),
                  'domain': act['kwargs'],
                  'runtime': datetime.now() - (datetime.fromtimestamp(time() - (monotonic() - act['time_start']))),
                  'logurl': '/static/logs/'+act['id']+'.log'
              } for act in raw_active]
    # act = raw_active[0]
    # active = {}
    # active['id'] = act['id']
    # active['pid'] = act['worker_pid']
    # active['start_time'] = datetime.fromtimestamp(time() - (monotonic() - act['time_start']))
    # active['domain'] = act['kwargs']
    # active['runtime'] = datetime.now() - active['start_time']
    # active['logurl'] = '/static/logs/'+act['id']+'.log'

    data = {'scheduled': [], 'active': active}
    return render_to_response('johnnywalker/home.html', data)
