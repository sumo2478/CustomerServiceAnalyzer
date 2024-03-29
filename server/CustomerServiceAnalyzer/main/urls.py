from django.conf.urls import patterns, url
from main import views

urlpatterns = patterns('',
        url(r'^$', views.info, name='info'),
        url(r'^info/$', views.info, name='info'),

        url(r'^homepage/$', views.homepage, name='homepage'),

        url(r'^login/$', views.login, name='login'),

        url(r'^login_request/$', views.login_request, name='login_request')
        )
