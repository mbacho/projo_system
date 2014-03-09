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

from os.path import join
from os import system, chdir, unlink
from shutil import rmtree

from celery import Task, task
from celery.utils.log import get_task_logger
from celery.result import AsyncResult
from django.conf import settings


logger = get_task_logger(__name__)


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
        projdir = settings.CRAWLER_DIRS['projdir']
        jobdir = settings.CRAWLER_DIRS['jobdir']
        logdir = settings.CRAWLER_DIRS['logdir']
        chdir(projdir)
        cmd = 'python manage.py scrapy crawl --logfile={0}.log '.format(join(logdir, self.request.id))
        cmd_args = ' -a start={0} -a domain={1} -a _job={2} -s JOBDIR={3} walker'
        cmd_args_s = cmd_args.format(starturl, domain, self.request.id, join(jobdir, self.request.id))
        logger.debug(cmd + cmd_args_s)
        system(cmd + cmd_args_s)


class CancelSpider(Task):
    def run(self, task_id, *args, **kwargs):
        #revoke task
        #delete files
        #delete stats/entry
        a = AsyncResult(task_id)
        a.revoke(terminate=True)
        jobdir = settings.CRAWLER_DIRS['jobdir']
        logdir = settings.CRAWLER_DIRS['logdir']

        try:
            rmtree(join(jobdir, task_id))
        except:
            pass

        try:
            unlink(join(logdir, (task_id + '.log')))
        except:
            pass

        return a
