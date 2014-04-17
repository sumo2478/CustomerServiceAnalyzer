from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

from .uploader import UploadFile

# Create your views here.
# TODO: Design an effective way to load large json files
def handle_uploaded_log(f):
	return 0

def upload_file(request):
	if request.method == 'POST':
		form = UploadFile(request.POST, request.FILES)
		if form.is_valid():
			handle_uploaded_log(request.FILES['file'])
			return HttpResponseRedirect(reverse('analyzer:analysis'))

	return HttpResponseRedirect('main:index')
