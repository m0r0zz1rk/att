from django import forms
from .models import AppCritFile

class UploadForm(forms.ModelForm):
    class Meta:
        model = AppCritFile
        fields = ('file',)
