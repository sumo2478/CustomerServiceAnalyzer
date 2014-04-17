from django import forms

class UploadFile(forms.Form):
    docfile  = forms.FileField(label="Select a file")
