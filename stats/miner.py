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

from collections import Counter
from json import loads

from os.path import (join )

from .models import DomainStats


RICHFILES = ['application/pdf', 'application/ps']


def get_domain_data(domain, datafolder):
    return join(datafolder, '%s.jsonlines' % domain)


def get_domain_outlink_data(domain, datafolder):
    return join(datafolder, '%s.outlinks.jsonlines' % domain)


def mine_data(domain, datafolder='johnnywalker/data/'):
    fyl = open(get_domain_data(domain, datafolder), 'r')
    domainlinks = [loads(i) for i in fyl.readlines()]
    fyl.close()
    fyl = open(get_domain_outlink_data(domain, datafolder), 'r')
    outlinks = [loads(i)['page'] for i in fyl.readlines()]
    fyl.close()

    stats = DomainStats()
    stats.domain = domain
    stats.outlinks = len(Counter(outlinks).keys())

    for i in domainlinks:
        if i['status'] == 200:
            stats.page_count += 1
            if i['type'] in RICHFILES:
                stats.richfiles += 1
        elif i['status'] == 404:
            stats.pages_not_found += 1

    return stats

def mine_details(domain):
    #mongodb aggregation
    pass