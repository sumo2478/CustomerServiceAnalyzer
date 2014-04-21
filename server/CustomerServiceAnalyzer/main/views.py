from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User # User authentication
from django.contrib.auth.decorators import login_required
from django.contrib import auth

from employee.models import Employee
from chat.models import Chat


# Create your views here.

#############################################################
# Index Views
#############################################################

def info(request):
    """Info Page - Homepage"""
    return render(request, 'main/info.html')

@login_required(login_url='/main/info')
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

    
