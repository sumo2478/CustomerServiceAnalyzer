from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

import constants

# Create your views here.
def render_chat_room(request, info):
	return render(request, 'chat/chat_room.html', {'info':info})

def employee_chat_room(request):
	info = {}
	info['id'] = 1
	info['name'] = "Collin Yen"
	info['entity_type'] = constants.ENTITY_TYPE_EMPLOYEE

	return render_chat_room(request, info)
    

def customer_chat_room(request):
	info = {}
	info['id'] = 2
	info['name'] = "Misa Campo"
	info['entity_type'] = constants.ENTITY_TYPE_CUSTOMER

	return render_chat_room(request, info)
