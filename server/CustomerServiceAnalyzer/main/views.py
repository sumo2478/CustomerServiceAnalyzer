from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User, Group # User authentication
from django.contrib.auth.decorators import login_required
from django.contrib import auth

from employee.models import Employee
from chat.models import Chat


# Create your views here.

#############################################################
# Index Views
#############################################################

def index(request):
    """Info Page - Homepage"""
    return render(request, 'main/index.html')

def create_employee(request):
    """ Create Employee Function """
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
            return HttpResponseRedirect(reverse('main:homepage'))

    return HttpResponseRedirect(reverse('main:homepage'))

def register_employee(request):
    """Employee Registration"""
    return render(request, 'main/registeremployee.html')

@login_required(login_url='/main/index')
def homepage(request):
    """Homepage"""
    return render(request, 'main/homepage.html')

def login(request):
    """Login Function"""
    return render(request, 'main/login.html')

def login_request(request):
    """Login Request"""
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('main:homepage'))
        else:
            # Return a disabled account error
            return render(request, 'main/login.html', {'error_message': "You're account has been disabled."})
    else:
        # Return an invalid login error message
        return render(request, 'main/login.html', {'error_message': "Invalid username/password"})

def base_login(request, redirect_page, return_error_page):
    """Base Login Request"""
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse(redirect_page))
        else:
            # Return a disabled account error
            return render(request, return_error_page, {'error_message': "You're account has been disabled."})
    else:
        # Return an invalid login error message
        return render(request, return_error_page, {'error_message': "Invalid username/password"})

def logout(request):
    """Logout Function"""
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:index'))

    
