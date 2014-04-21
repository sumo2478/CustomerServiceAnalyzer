from django.conf.urls import patterns, url
from employee import views
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',

	# Employee Home Page
	url(r'^$', views.home, name='home'),
	url(r'^home/$', views.home, name='home'),

	# Employee Info Page
	url(r'^info/$', views.info, name='info'),

	# Login Page
	url(r'^login/$', views.login, name='login'),

	# Login Request Function
	url(r'^login_request/$', views.login_request, name='login_request'),

	# Logout Function
	url(r'^logout/$', views.logout, name='logout'),

	# Register Employee Page
	url(r'^register/$', views.register, name='register'),

	# Register Employee Function
	url(r'^create_employee/$', views.create_employee, name='create_employee')

	
	)