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


from django.http import HttpResponse
import mimetypes
import urllib2

def graph(request):
    url = 'http://127.0.0.1:81/render'
    if request.META.has_key('QUERY_STRING'):
        url += '?' + request.META['QUERY_STRING']
    try:
        proxied_request = urllib2.urlopen(url)
        status_code = proxied_request.code
        mimetype = proxied_request.headers.typeheader or mimetypes.guess_type(url)
        content = proxied_request.read()
    except urllib2.HTTPError as e:
        return HttpResponse(e.msg, status=e.code, mimetype='text/plain')
    else:
        return HttpResponse(content, status=status_code, mimetype=mimetype)
