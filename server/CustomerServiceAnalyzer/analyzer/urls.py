from django.conf.urls import patterns, url
from analyzer import views

urlpatterns = patterns('',
        url(r'^upload/$', views.upload, name='upload'),

        url(r'^upload_file/$', views.upload_file, name='upload_file') ,

        url(r'^analyze/$', views.analyze, name='analyze'),

        url(r'^analysis/(?P<chat_id>\d+)/$', views.analysis, name='analysis')
        )
