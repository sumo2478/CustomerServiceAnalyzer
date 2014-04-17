from django.conf.urls import patterns, url
from main import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),

        url(r'^index/$', views.index, name='index'),

        url(r'^registeremployee/$', views.register_employee, name='registeremployee'),

        url(r'^createemployee/$', views.create_employee, name='createemployee'),

        url(r'^homepage/$', views.homepage, name='homepage'),

        url(r'^logout/$', views.logout, name='logout')  
        )
