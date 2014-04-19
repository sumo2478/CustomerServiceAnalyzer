from django.conf.urls import patterns, url
from employee import views
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',

	# Employee Index Page
	url(r'^$', views.info, name='info'),
	url(r'^employee/$', views.info, name='info'),

	# Login Page
	url(r'^login/$', views.login, name='login'),

	# Login Request Function
	url(r'^login_request/$', views.login_request, name='login_request'),

	# Home Page
	url(r'^home/$', views.home, name='home')
	)