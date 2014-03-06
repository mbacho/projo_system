# Create your views here.

from django.contrib.auth import (authenticate, login, logout)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from webui.forms import (SigninForm, SignupForm)
from webui.models import Project


@login_required(login_url='signin')
def home(request):
    # return render_to_response('webui/index.html', {'user': request.user})
    projos = Project.objects.filter(owner=request.user)
    return render_to_response('webui/project/list.html',
                              {'projects': projos, 'user': request.user, 'active': 'projects'})


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
    return render_to_response('webui/signin.html', {'frm': frm, 'nextpage': nextpage},
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

    return render_to_response('webui/signin.html', {'frm': frm, 'signup': True, },
                              context_instance=RequestContext(request))

