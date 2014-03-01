# Create your views here.
from datetime import datetime
from django.shortcuts import render_to_response
from scrapyd import Config
from scrapyd.launcher import Launcher
from scrapyd.poller import QueuePoller


def get_log_url(self, jobid):
    return "/static/items/johnnywalker/walker/{0}.log".format(jobid)


def get_items_url(self, jobid):
    return "/static/items/johnnywalker/walker/{0}.jl".format(jobid)


def home(request):
    config = Config()
    poller = QueuePoller(config)
    queue_list = poller.queues.items()[-1]
    queue_list = queue_list[1].list()
    launcher = Launcher(config, None)
    pending = [{
                   'name': i['name'],
                   'job': i['_job']
               } for i in queue_list]
    running = [{
                   'job': i['job'],
                   'pid': i['pid'],
                   'runtime': datetime.now() - i['start_time'],
                   'log_url': get_log_url(i['job']),
                   'items_url': get_items_url(i['job'])
               } for i in launcher.processes.values()]
    finished = [{
                    'job': i['job'],
                    'runtime': i['end_time'] - i['start_time'],
                    'log_url': get_log_url(i['job']),
                    'items_url': get_items_url(i['job'])
                } for i in launcher.finished]
    data = {
        'pending': pending,
        'running': running,
        'finished': finished
    }
    return render_to_response('johnnywalker/home.html', data)
