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
from celery import Task
from core import mail_user
from stats.miner import Miner, HistoryMiner
from webui.models import ProjectDomain


class MinerTask(Task):
    def run(self, collection_name, project_domain_id, *args, **kwargs):
        pd = ProjectDomain.objects.get(id=project_domain_id)
        miner = Miner(collection_name, pd)
        miner.webometric()
        pagerank = miner.pagerank()
        msg = 'preliminary statistics for the domain {0} have been done'
        mail_user(pd.project.owner.email, msg.format(pd.domain.domain), )


class HistoryMinerTask(Task):
    def run(self, project_domain_id, *args, **kwargs):
        pd = ProjectDomain.objects.get(id=project_domain_id)
        miner = HistoryMiner(pd)
        hist = miner.get_history()


class DownloadTask(Task):
    def run(self, collection_name, project_domain, *args, **kwargs):
        # download stats as csv
        pass
