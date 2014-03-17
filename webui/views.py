# Create your views here.

from json import dumps

from django.contrib.auth import (authenticate, login, logout)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from webui.forms import (SigninForm, SignupForm, ProjectForm)
from webui.models import Project, ProjectDomain
from webui.tasks import DeleteProject


@login_required(login_url='signin')
def home(request):
    projos = Project.objects.filter(owner=request.user)
    return render_to_response('webui/project/list.html',
                              {'projects': projos, 'active': 'projects'},
                              context_instance=RequestContext(request))


def signin(request):
    frm = SigninForm(request.POST or None)

    if frm.is_valid():
        username = frm.cleaned_data['username']
        password = frm.cleaned_data['password']
        nextpage = frm.cleaned_data['nextpage']
        u = authenticate(username=username, password=password)
        if u is None:
            frm.errors['login_error'] = 'username/password combination invalid'
        if len(frm.errors) == 0:
            if u.is_active:
                login(request, u)
                return HttpResponseRedirect(reverse('home') if nextpage in [None, '']else nextpage)
            else:
                frm.errors['account_error'] = 'account not activated'

    nextpage = request.GET['next'] if 'next' in request.GET else ''
    return render_to_response('webui/signin.html', {'frm': frm, 'nextpage': nextpage, 'active': 'signin'},
                              context_instance=RequestContext(request))


def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse('signin'))


def signup(request):
    frm = SignupForm(request.POST or None)
    if frm.is_valid():
        username = frm.cleaned_data['username']
        password = frm.cleaned_data['password']
        password_confirm = frm.cleaned_data['password_confirm']
        errors = []
        if password != password_confirm:
            errors.append('passwords don\'t match')

        email = frm.cleaned_data['email']
        u = User.objects.create_user(username, email, password)
        u.is_active = False
        u.save()
        #email_confirm_link(request, u)
        return HttpResponseRedirect(reverse('signin'))

    return render_to_response('webui/signin.html', {'frm': frm, 'signup': True, 'active': 'signup'},
                              context_instance=RequestContext(request))


@login_required(login_url='signin')
def user(request):
    return render_to_response('webui/user.html', {'active': 'user'}, context_instance=RequestContext(request))


@login_required(login_url='signin')
def project(request, pk=None):
    projos = Project.objects.filter(owner=request.user)
    data = {'projects': projos, 'active': 'projects'}
    if pk is not None:
        pr = Project.objects.get(id=pk, owner=request.user)
        pd = ProjectDomain.objects.filter(project=pr)
        data['projectdomains'] = pd
        data['active_project'] = pr
    return render_to_response('webui/project/list.html', data, context_instance=RequestContext(request))


@login_required(login_url='signin')
def project_edit(request, pk=None):
    frm = ProjectForm(request.POST or None)
    if frm.is_valid():
        proj_name = frm.cleaned_data['project_name']
        proj = None
        if pk is None:
            proj, created = Project.objects.get_or_create(name=proj_name, owner=request.user)
            if not created:
                raise IntegrityError('project %s already exists' % proj_name)
        else:
            proj = Project.objects.get(id=pk)
            proj.name = proj_name
            proj.save()

        return HttpResponseRedirect(reverse('project_det', args=[proj.id]))

    else:
        #TODO Catch this
        pass


@login_required(login_url='signin')
def project_del(request, pk):
    projdel = DeleteProject()
    async = projdel.delay(project_id=pk)
    return HttpResponse(content=dumps({'task': async.task_id, 'status': 'deletion scheduled'}),
                        mimetype='application/json')

