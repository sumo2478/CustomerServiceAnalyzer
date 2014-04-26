from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from django.contrib.auth.models import User

import constants

# Create your views here.
# def render_chat_room(request, info):
# 	return render(request, 'chat/chat_room.html', {'info':info})

def employee_chat_room(request):
	info = {}
	info['id'] = request.user.id
	info['name'] = request.user.get_full_name()
	info['entity_type'] = constants.ENTITY_TYPE_EMPLOYEE

	return render(request, 'chat/employee_chat_room.html', {'info': info})
    
def customer_chat_room(request):
	info = {}
	info['id'] = 2
	info['name'] = "Customer"
	info['entity_type'] = constants.ENTITY_TYPE_CUSTOMER

	return render(request, 'chat/customer_chat_room.html', {'info':info})
