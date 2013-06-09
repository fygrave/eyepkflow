# project wide urls
from django.conf.urls import patterns, include, url
#from django.views.generic.simple import redirect_to
from django.views.generic import TemplateView, RedirectView
from django.core.urlresolvers import reverse
from django.contrib import admin

admin.autodiscover()
import settings

# import your urls from each app here, as needed
import ddosui.urls

urlpatterns = patterns('',

    # urls specific to this app
    url(r'^login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
#    url(r'^logout/$', 'ddoslyzer.ddosui.views.logout_page'),
#    url(r'^accounts/', include(registration.urls)),
    url(r'^ddosui/', include(ddosui.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # catch all, redirect to ddosui home view
    url(r'.*', RedirectView.as_view(url='/ddosui/home')),

)
