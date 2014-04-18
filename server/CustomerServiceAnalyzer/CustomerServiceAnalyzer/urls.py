from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^main/', include('main.urls', namespace="main")),
    url(r'^analyzer/', include('analyzer.urls', namespace="analyzer")),
    url(r'^chat/', include('chat.urls', namespace="chat"))
)
