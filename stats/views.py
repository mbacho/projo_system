# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from webui.models import Project


@login_required(login_url='signin')
def results(request, pk=None):
    projos = Project.objects.filter(owner=request.user)
    data = {'projects': projos, 'active': 'results'}
    if pk is not None:
        pr = Project.objects.get(id=pk, owner=request.user)
        data['active_project'] = pr

    return render_to_response('stats/list.html', data, context_instance=RequestContext(request))
