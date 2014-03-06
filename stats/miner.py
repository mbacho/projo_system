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

from johnnywalker.models import RichFile
from .models import DomainStats
from webui.models import ProjectDomain


def mine_data(collection_name, project_domain):
    dbname = settings.MONGO_DB['name']
    collection_links = settings.MONGO_DB['link_collection']
    collection_outlinks = settings.MONGO_DB['outlink_collection']
    rich_files = [x.type for x in RichFile.objects.all()]

    client = MongoClient()
    db = client[dbname]
    links = db[collection_links][collection_name]
    if links.name not in db.collection_names():
        raise ValueError('no data found for collection %s' % collection_name)
    outlinks = db[collection_outlinks][collection_name]

    stats = DomainStats()
    stats.projectdomain = project_domain
    stats.page_count = links.find({'status': 200}).count()
    stats.pages_not_found = links.find({'status': 404}).count()
    stats.richfiles = links.find({'type': {'$in': rich_files}, 'status': 200}).count()
    stats.outlinks = len(outlinks.distinct('page'))
    stats.save()

    return stats


def history_miner(academic_domain, owner):
    project_domains = ProjectDomain.objects.filter(domain=academic_domain, project__owner=owner)
    domain_stats = DomainStats.objects.filter(projectdomain__in=project_domains).order_by('created')

    return domain_stats

