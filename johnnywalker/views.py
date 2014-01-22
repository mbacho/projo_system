# Create your views here.
from json import loads

from urllib2 import urlopen

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.http import urlencode

from johnnywalker.forms import StartCrawlForm


class ScrapydCommunicator(object):
    host = '127.0.0.1'
    port = 6880

    def __init__(self):
        pass

    def _get_jsondata(self, apicall, method, arguments=None):
        url = "http://{0}:{1}/{2}.json".format(self.host, self.port, apicall)
        data_encoded = urlencode(arguments) if type(arguments) is dict else ""
        if method in ['POST', 'post']:
            return loads(urlopen(url, data_encoded).read())
        else:
            data = url + ("?" + data_encoded) if len(data_encoded) > 0 else ""
            return loads(urlopen(url).read())

    def listprojects(self):
        """
        GET
        sample response: {"status": "ok", "projects": ["myproject", "otherproject"]}
        """
        return self._get_jsondata('listprojects', 'GET')

    def addversion(self):
        """
        POST
        - project (string, required) - the project name
        - version (string, required) - the project version
        - egg (file, required) - a Python egg containing the project's code

        sample response : {"status": "ok", "spiders": 3}
        """
        pass

    def schedule(self):
        """
        POST
        - project (string, required) - the project name
        - spider (string, required) - the spider name
        - setting (string, optional) - a scrapy setting to use when running the spider
        - any other parameter is passed as spider argument

        sample response: {"status": "ok", "jobid": "6487ec79947edab326d6db28a2d86511e8247444"}
        """
        pass

    def cancel(self):
        """
        POST
        - project (string, required) - the project name
        - job (string, required) - the job id
        sample response: {"status": "ok", "prevstate": "running"}
        """

    def listversions(self):
        """
        GET
        - project (string, required) - the project name
        sample response: {"status": "ok", "versions": ["r99", "r156"]}
        """
        pass

    def listspiders(self):
        """
        GET
        - project (string, required) - the project name
        sample response: {"status": "ok", "spiders": ["spider1", "spider2", "spider3"]}
        """
        pass

    def listjobs(self):
        """
        GET
        - project (string, required) - the project name
        sample response: {"status": "ok",
        "pending": [{"id": "78391cc0fcaf11e1b0090800272a6d06", "spider": "spider1"}],
        "running": [{"id": "422e608f9f28cef127b3d5ef93fe9399", "spider": "spider2", "start_time": "2012-09-1
        "finished": [{"id": "2f16646cfcaf11e1b0090800272a6d06", "spider": "spider3", "start_time": "2012-09-
        """
        pass

    def delversion(self):
        """
        POST
        - project (string, required) - the project name
        - version (string, required) - the project version
        sample response: {"status": "ok"}
        """
        pass

    def delproject(self):
        """
        POST
        - project (string, required) - the project name

        sample response: {"status": "ok"}
        """
        pass


def home(request):
    frm = StartCrawlForm(request.POST or None)
    comms = ScrapydCommunicator()
    projects = comms.listprojects()
    if frm.is_valid():
        startpage, domain = frm.cleaned_data['startpage'], frm.cleaned_data['domain']
        return render_to_response('johnnywalker/home.html', {'active_spiders': projects})

    return render_to_response('johnnywalker/home.html', {'startcrawlform': frm, 'active_spiders': projects},
                              context_instance=RequestContext(request))


def start(request):
    return HttpResponse('spider started')


def pause(request):
    pass


