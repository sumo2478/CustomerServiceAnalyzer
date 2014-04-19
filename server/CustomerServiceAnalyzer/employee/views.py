from django.shortcuts import render

from main.views import base_login

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User # User authentication
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import auth
# Create your views here.

def authenticate_employee(user):
	return user.is_authenticated() and user.groups.filter(name='Employee').exists()

def info(request):
	"""Index Page"""
	return render(request, 'employee/info.html')

def login(request):
	"""Login Page"""
	return render(request, 'employee/login.html')

def login_request(request):
	""" Employee Login Request """
	return base_login(request, 'employee:home', 'employee/login.html')

@user_passes_test(authenticate_employee, login_url='employee:login')
def home(request):
	"""Home Page"""
	return render(request, 'employee/home.html')