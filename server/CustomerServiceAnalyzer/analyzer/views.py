from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

from .uploader import UploadFile
from main import views

from employee.models import EmployeeChatList, Employee
from chat.models import Chat

import json
from analyzerClass import Analyzer

# Create your views here.
# TODO: Design an effective way to load large json files
def handle_uploaded_log(f, employee_id):
	# Load the json file
	log = json.load(f)
	customer_name = log[0]['customer_name']

	# Create a new chat entry for the employee
	employee = Employee.objects.get(user__id = employee_id)
	employee_entry = EmployeeChatList(employee=employee, customer_name=customer_name)
	employee_entry.save()

	chat_id = employee_entry.chat_id

	total_score = 0 # The running score of the entire chat

	analyzer = Analyzer()

	# For each entry in the log store it
	for entry in log[1:]:
		if entry['is_employee']:
			message = Chat(chat_id=chat_id, message=entry['message'], is_employee=entry['is_employee'])
			message.save()
		else:
			score = analyzer.analyze_and_store_message(chat_id, entry)
			total_score += score
		
	employee_entry.score = total_score
	employee_entry.save()

	return
	
def upload_file(request):
	if request.method == 'POST':
		form = UploadFile(request.POST, request.FILES)
		if form.is_valid():
			handle_uploaded_log(request.FILES['docfile'], request.user.id)
			#return HttpResponseRedirect(reverse('analyzer:analysis'))
			return HttpResponseRedirect('/main/registeremployee')

	return HttpResponseRedirect('/main/index')

def upload(request):
	form = UploadFile()
	return render(request, 'analyzer/upload.html', {'form':form})