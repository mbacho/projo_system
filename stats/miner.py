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


file : miner.py
project : webometrics

"""

from pymongo import MongoClient
from django.conf import settings
from networkx import DiGraph
from networkx.algorithms.link_analysis import pagerank as pr
from pymongo.collection import Collection

from johnnywalker.models import RichFile
from .models import DomainStats


class Miner(object):
    def __init__(self, collection_name, project_domain):
        dbname = settings.MONGO_DB['name']
        collection_links = settings.MONGO_DB['link_collection']
        collection_outlinks = settings.MONGO_DB['outlink_collection']
        self.rich_files = [x.type for x in RichFile.objects.all()]

        client = MongoClient()
        db = client[dbname]
        self.links = db[collection_links][collection_name]
        if self.links.name not in db.collection_names():
            raise ValueError('no data found for collection %s' % collection_name)
        self.outlinks = db[collection_outlinks][collection_name]
        self.project_domain = project_domain

    def webometric(self):
        stats = DomainStats()
        stats.projectdomain = self.project_domain
        stats.page_count = self.links.find({'status': 200}).count()
        stats.pages_not_found = self.links.find({'status': 404}).count()
        stats.richfiles = self.links.find({'type': {'$in': self.rich_files}, 'status': 200}).count()
        stats.outlinks = len(self.outlinks.distinct('page'))
        stats.save()
        #TODO Add G-factor
        return stats

    def pagerank(self):
        g = DiGraph()
        valid_links = self.links.find({'status': 200})
        outlinks = self.outlinks
        for i in valid_links:
            g.add_edge(i['parent'], i['page'])
        for i in outlinks.find(): #TODO remove stupid hack
            g.add_edge(i['parent'], i['page'])
        return pr(g)

    def history_miner(self):
        pass

