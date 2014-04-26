from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User, Group # User authentication
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import auth

from employee.models import Employee
from main.views import base_login

def authenticate_employee(user):
	"""Checks to make sure authorized employee is logged in"""
	return user.is_authenticated() and user.groups.filter(name='Employee').exists()

def login(request):
	"""Login Page"""
	return render(request, 'employee/login.html')

def login_request(request):
	""" Employee Login Request """
	return base_login(request, 'employee:home', 'employee/login.html')

def logout(request):
	"""Logout Function"""
	auth.logout(request)
	return HttpResponseRedirect(reverse('employee:info'))

def register(request):
	"""Register Employee"""
	return render(request, 'employee/register.html')

def create_employee(request):
	"""Create Employee"""
	username = request.POST['username']
	password = request.POST['password']
	confirm_password = request.POST['confirm_password']
	first_name = request.POST['first_name']
	last_name  = request.POST['last_name']

	# TODO: Add password verification

	u = User.objects.create_user(username=username,
	                             password=password,
	                             email=username,
	                             first_name=first_name,
	                             last_name=last_name)

	# Add the user ot the Employee group
	groupid, group = Group.objects.get_or_create(name="Employee")
	u.groups.add(groupid)

	# Create the Employee
	e = Employee(user=u)
	e.save()

	user = auth.authenticate(username=username, password=password)

	if user is not None:
	    if user.is_active:
	        auth.login(request, user)
	        return HttpResponseRedirect(reverse('employee:home'))

	return HttpResponseRedirect(reverse('employee:home'))

def info(request):
	"""Index Page"""
	return render(request, 'employee/info.html')

# Get employee helper function
def get_employee(user_id):
	return get_object_or_404(Employee, user__id=user_id)

@user_passes_test(authenticate_employee, login_url='employee:info')
def home(request):
	"""Home Page"""
	# Retrieve the correct employee
	employee = get_employee(request.user.id)
	recent_sessions = employee.retrieve_recent_sessions()

	params = {}
	params['employee'] = employee
	params['recent_sessions'] = recent_sessions
	params['customers_helped'] = employee.num_recent_customers()
	return render(request, 'employee/home.html', params)