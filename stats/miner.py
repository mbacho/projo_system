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
from .models import DomainStats
from johnnywalker import (MONGO_DBNAME, MONGO_COLLECTION_LINKS, MONGO_COLLECTION_OUTLINKS, RICH_FILES)


def mine_data(domain):
    client = MongoClient()
    db = client[MONGO_DBNAME]
    links = db[MONGO_COLLECTION_LINKS][domain]
    if links.name not in db.collection_names():
        raise ValueError('no data found for domain %s' % domain)
    outlinks = db[MONGO_COLLECTION_OUTLINKS][domain]

    stats = DomainStats()
    stats.domain = domain
    stats.page_count = links.find({'status': 200}).count()
    stats.pages_not_found = links.find({'status': 404}).count()
    stats.richfiles = links.find({'type': {'$in': RICH_FILES.values()}, 'status': 200}).count()
    stats.outlinks = len(outlinks.distinct('page'))

    return stats

