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


file : comm.py
project : webometrics

"""

from json import loads
from urllib2 import urlopen
from urlparse import urljoin
from django.utils.http import urlencode


class ScrapydCommunicator(object):
    host = 'localhost'
    port = 6880
    spider = 'walker'
    project = 'johnnywalker'

    def __init__(self):
        pass

    def _get_jsondata(self, apicall, method, arguments=None):
        url = "http://{0}:{1}/{2}.json".format(self.host, self.port, apicall)
        try:
            data_encoded = urlencode(arguments) if type(arguments) is dict else ""
            if method in ['POST', 'post']:
                return loads(urlopen(url, data_encoded).read())
            else:
                data = ("?" + data_encoded) if len(data_encoded) > 0 else ""
                return loads(urlopen(urljoin(url, data)).read())
        except Exception, ex:
            return {'status':'error', 'message':'server connection error', 'exception':ex.message }

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

    def schedule(self, startpage, domain):
        """
        POST
        - project (string, required) - the project name
        - spider (string, required) - the spider name
        - setting (string, optional) - a scrapy setting to use when running the spider
        - any other parameter is passed as spider argument

        sample response: {"status": "ok", "jobid": "6487ec79947edab326d6db28a2d86511e8247444"}
        """
        return self._get_jsondata('schedule', 'post',
                                  {'project': self.project, "spider": self.spider,
                                   "start": startpage, "domain": domain
                                  })

    def cancel(self, jobid):
        """
        POST
        - project (string, required) - the project name
        - job (string, required) - the job id
        sample response: {"status": "ok", "prevstate": "running"}
        """
        return self._get_jsondata('cancel', 'post', {'project': self.project, 'job': jobid})

    def listversions(self):
        """
        GET
        - project (string, required) - the project name
        sample response: {"status": "ok", "versions": ["r99", "r156"]}
        """
        return self._get_jsondata('listversions', 'get', {'project': self.project})

    def listspiders(self):
        """
        GET
        - project (string, required) - the project name
        sample response: {"status": "ok", "spiders": ["spider1", "spider2", "spider3"]}
        """
        return self._get_jsondata('listspiders', 'get', {'project': self.project})

    def listjobs(self):
        """
        GET
        - project (string, required) - the project name
        sample response: {"status": "ok",
        "pending": [{"id": "78391cc0fcaf11e1b0090800272a6d06", "spider": "spider1"}],
        "running": [{"id": "422e608f9f28cef127b3d5ef93fe9399", "spider": "spider2", "start_time": "2012-09-1
        "finished": [{"id": "2f16646cfcaf11e1b0090800272a6d06", "spider": "spider3", "start_time": "2012-09-
        """
        return self._get_jsondata('listjobs', 'get', {'project': self.project})

    def delversion(self, version):
        """
        POST
        - project (string, required) - the project name
        - version (string, required) - the project version
        sample response: {"status": "ok"}
        """
        return self._get_jsondata('delversion', 'get', {'project': self.project, 'version': version})

    def delproject(self):
        """
        POST
        - project (string, required) - the project name

        sample response: {"status": "ok"}
        """
        return self._get_jsondata('delproject', 'get', {'project': self.project})

