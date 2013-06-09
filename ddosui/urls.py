# app specific urls
from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


urlpatterns = patterns('',
    url(r'^home', 'ddosui.views.home'),
    url(r'^alerts', 'ddosui.views.alerts'),
    url(r'^system', 'ddosui.views.system'),
    url(r'^logout', 'ddosui.views.logout'),
)
