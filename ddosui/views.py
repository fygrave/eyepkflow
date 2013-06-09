from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth import logout

@login_required
def home(request):

    d = RequestContext(request,{'navigation': 'dashboard'})


    return render_to_response('home.html', d)


@login_required
def alerts(request):

    d = RequestContext(request,{'navigation': 'alerts'})


    return render_to_response('alerts.html', d)


@login_required
def system(request):

    d = RequestContext(request,{'navigation': 'system'})


    return render_to_response('system.html', d)

@login_required
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


