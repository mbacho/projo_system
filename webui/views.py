# Create your views here.
from django.contrib.auth import (authenticate, login, logout)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.timezone import now
from json import dumps
from core.comm import ScrapydCommunicator
from webui.forms import (SigninForm, SignupForm)
from webui.models import Project, ProjectDomain


@login_required(login_url='signin')
def home(request):
    # return render_to_response('webui/index.html', {'user': request.user})
    projos = Project.objects.filter(owner=request.user)
    return render_to_response('webui/project/list.html',
                              {'projects': projos, 'user': request.user, 'active': 'projects'})


#@login_not_required(redirect_url='home')
def signin(request):
    frm = SigninForm(request.POST or None)
    if frm.is_valid():
        username = frm.cleaned_data['username']
        password = frm.cleaned_data['password']
        nextpage = frm.cleaned_data['nextpage']
        u = authenticate(username=username, password=password)
        errs = []
        if u is None:
            errs.append('username/password combination invalid')
        if errs is not None and not u.is_active:
            errs.append('account not activated')
        if len(errs) == 0:
            login(request, u)
            return HttpResponseRedirect(reverse('home') if nextpage in [None, '']else nextpage)

    nextpage = request.GET['next'] if 'next' in request.GET else ''
    return render_to_response('webui/signin.html', {'frm': frm, 'nextpage': nextpage},
                              context_instance=RequestContext(request))


#@login_not_required(redirect_url='home')
def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse('signin'))


def signup(request):
    frm = SignupForm(request.POST or None)
    if frm.is_valid():
        username = frm.cleaned_data['username']
        password = frm.cleaned_data['password']
        password_confirm = frm.cleaned_data['password_confirm']
        email = frm.cleaned_data['email']
        u = User.objects.create_user(username, email, password)
        u.is_active = False
        u.save()
        #email_confirm_link(request, u)
        login(request, user=u)

    return render_to_response('webui/signin.html', {'frm': frm, 'signup': True, },
                              context_instance=RequestContext(request))


@login_required(login_url='signin')
def project_new(request, name):
    name = request.GET.get('name', None)
    domain = request.GET.get('domain', None)
    starturl = request.GET.get('starturl', None)
    subdomain = request.GET.get('subdomain', None)

    comm = ScrapydCommunicator()
    j = comm.schedule(startpage=starturl, domain=domain)
    if j['status'] == 'ok':
        p = Project()
        p.name = name
        p.owner = request.user
        p.save()

        pd = ProjectDomain()
        pd.project = p
        pd.subdomain = subdomain
        pd.domain_id = domain
        pd.jobid = j['jobid']
        pd.starttime = now()
        pd.starturl = starturl
        pd.save()

    return HttpResponse(content_type='application/json', content=dumps(j))



@login_required(login_url='signin')
def project_edit(request, name):
    return HttpResponse(content='project del %s' % name)


@login_required(login_url='signin')
def project_del(request, name):
    return HttpResponse(content='project del %s' % name)

@login_required(login_url='signin')
def results(request):
    return render_to_response('_base.html', {'user':request.user,'active':'results'})

