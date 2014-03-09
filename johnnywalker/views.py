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
    # active = [{
    #               'id': act['id'],
    #               'pid': act['worker_pid'],
    #               'start_time': act['time_start'],
    #               'domain': act['kwargs'],
    #               'runtime': act['time_start']
    #               'logurl': 'log_url'
    #           } for act in raw_active]
    act = raw_active[0]
    active = {}
    active['id'] = act['id']
    active['pid'] = act['worker_pid']
    active['start_time'] = datetime.fromtimestamp(time() - (monotonic() - act['time_start']))
    active['domain'] = act['kwargs']
    active['runtime'] = datetime.now() - active['start_time']
    active['logurl'] = 'log_url'

    data = {'scheduled': [], 'active': [active]}
    return render_to_response('johnnywalker/home.html', data)
