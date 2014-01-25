# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from core.comm import ScrapydCommunicator

from johnnywalker.forms import StartCrawlForm


def home(request):
    frm = StartCrawlForm(request.POST or None)
    comms = ScrapydCommunicator()
    projects = comms.listprojects()
    jobs = comms.listjobs()
    status = {}
    if frm.is_valid():
        startpage, domain = frm.cleaned_data['startpage'], frm.cleaned_data['domain']
        status = comms.schedule(startpage, domain)

    return render_to_response('johnnywalker/home.html',
                              {'startcrawlform': frm, 'projects': projects, 'jobs': jobs, 'status': status},
                              context_instance=RequestContext(request))

