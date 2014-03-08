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


file : tasks.py
project : webometrics

"""

from celery import Task, task
from scrapy.crawler import Crawler
from scrapy.conf import get_project_settings

from johnnywalker.spiders.walker import Walker


@task(bind=True, name='crawler_server.debug_task')
def debug_task(self):
    """Test method"""
    return "debug_task"


class DebugTask(Task):
    """Test class"""
    name = 'crawler_server.DebugTask'

    def run(self, *args, **kwargs):
        return "debug_class"


class RunSpider(Task):
    def run(self, domain, starturl, *args, **kwargs):
        # jobdir = dirname(join(abspath(manage.__file__), 'jobs'))
        from nose.tools import set_trace

        set_trace()
        # cmd = 'python manage.py scrapy crawl walker '
        # cmd_args = '-a start={0} -a domain={1} -a _job={2} -s JOBDIR={3}'
        # cmd_args_s = cmd_args.format(starturl, domain, self.request.id, "jobdir/" + self.request.id)
        # system(cmd + cmd_args_s)
        spider = Walker(starturl, domain, self.request.id)
        crawler = Crawler(get_project_settings())
        crawler.crawl(spider)


class CancelSpiderRun(Task):
    def run(self, job_id, *args, **kwargs):
        #revoke task
        #delete files
        #delete stats/entry
        pass

