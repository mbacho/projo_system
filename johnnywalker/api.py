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


file : api.py
project : webometrics

"""
from tastypie.resources import (Resource)
from core.comm import ScrapydCommunicator


class CrawlerProjectResource(Resource):
    comm = ScrapydCommunicator()

    class Meta:
        resource_name = 'crawler'

    def schedule(self, startpage, domain):
        return self.comm.schedule(startpage, domain)

    def cancel(self, jobid):
        return self.comm.cancel(jobid)

    def listjobs(self):
        return self.comm.listjobs()

    def detail_uri_kwargs(self):
        pass

    def get_object_list(self):
        pass

    def obj_get_list(self):
        pass

    def obj_get(self):
        pass

    def obj_create(self):
        pass

    def obj_update(self):
        pass

    def obj_delete_list(self):
        pass

    def obj_delete(self):
        pass

    def rollback(self):
        pass