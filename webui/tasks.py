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
from genericpath import exists
from os import unlink
from os.path import join
from shutil import rmtree

from celery import Task
from django.conf import settings
from pymongo import MongoClient

from webui.models import Project, ProjectDomain


class DeleteProject(Task):
    def drop_mongo_collections(self, project_domains):
        dbname = settings.MONGO_DB['name']
        collection_outlinks = settings.MONGO_DB['outlink_collection']
        collection_links = settings.MONGO_DB['link_collection']
        client = MongoClient()
        db = client[dbname]
        for i in project_domains:
            coll = db[collection_links][i.get_collection_name]
            db.drop_collection(coll.name)
            coll = db[collection_outlinks][i.get_collection_name]
            db.drop_collection(coll.name)
            if i.jobid:
                self.drop_jobs_logs(i.jobid)

    def drop_jobs_logs(self, taskid):
        jobdir = join(settings.CRAWLER_DIRS['jobdir'], taskid)
        logfile = join(settings.CRAWLER_DIRS['logdir'], '%s.log' % taskid)
        if exists(jobdir):
            rmtree(jobdir)

        if exists(logfile):
            unlink(logfile)

    def run(self, project_id, *args, **kwargs):
        projo = Project.objects.get(id=project_id)
        project_domains = ProjectDomain.objects.filter(project=projo)
        self.drop_mongo_collections(project_domains)
        project_domains.delete()
        projo.delete()


class DeleteProjectDomain(Task):
    def run(self, project_domain_id, *args, **kwargs):
        pass
