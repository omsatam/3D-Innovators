from django import forms

class UploadFileForm(forms.Form):
    path = forms.CharField(required=False)
    CT_data = forms.FileField(widget = forms.ClearableFileInput(attrs={'multiple' : True}))