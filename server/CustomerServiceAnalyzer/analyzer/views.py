from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, get_object_or_404
from django.core.urlresolvers import reverse

from .uploader import UploadFile
from main import views

from employee.models import EmployeeChatList, Employee
from employee.views  import get_employee
from chat.models import Chat

import json
from analyzerClass import Analyzer

# Create your views here.
# TODO: Design an effective way to load large json files
def handle_uploaded_log(f, employee_id):
	"""
	Given a chat log json file it sends it to the analyzer to be 
	analyzed and stored in the database
	"""
	# Load the json file
	log = json.load(f)
	customer_name = log[0]['customer_name']

	# Create a new chat entry for the employee
	employee = Employee.objects.get(user__id = employee_id)
	employee_entry = EmployeeChatList(employee=employee, customer_name=customer_name)
	employee_entry.save()

	chat_id = employee_entry.chat_id

	analyzer = Analyzer()

	total_score = 0 # The running score of the entire chat

	# For each entry in the log except for the first one which contains the customer name store it
	for entry in log[1:]:
		if entry['is_employee']:
			message = Chat(chat_id=chat_id, message=entry['message'], is_employee=entry['is_employee'])
			message.save()
		else:
			score = analyzer.analyze_and_store_message(chat_id, entry)
			total_score += score
		
	employee_entry.score = total_score
	employee_entry.save()

	return chat_id
	
def upload_file(request):
	"""Upload File Function"""
	if request.method == 'POST':
		form = UploadFile(request.POST, request.FILES)
		if form.is_valid():
			chat_id = handle_uploaded_log(request.FILES['docfile'], request.user.id)
			return HttpResponseRedirect(reverse('analyzer:analysis', kwargs={'chat_id':chat_id}))

	# If the request is not a POST or correct file is not submitted then return back to upload page with error
	return HttpResponseRedirect(reverse('analyzer:upload'), {'error':'Invalid file submitted'})

def upload(request):
	"""Upload Page"""
	form = UploadFile()
	return render(request, 'analyzer/upload.html', {'form':form})

def analyze(request):
	params = request.POST

	analyzer = Analyzer()
	messages = analyzer.analyze_chat_log(params['chat_id'])

	url = reverse('analyzer:analysis', kwargs={'chat_id':params['chat_id']})
	return HttpResponseRedirect(url)

def analysis(request, chat_id):
	"""Analysis Page"""
	employee = get_employee(request.user.id)
	messages = Chat.objects.filter(chat_id=chat_id)
	employee_chat_list    = get_object_or_404(EmployeeChatList, chat_id=chat_id)
	analyzer = Analyzer()

	params = {}
	params['messages'] = messages
	params['employee'] = employee
	params['chat_id']  = chat_id
	params['histogram'] = analyzer.create_histogram(messages)
	params['score']     = employee_chat_list.score
	return render(request, 'analyzer/analysis.html', params)