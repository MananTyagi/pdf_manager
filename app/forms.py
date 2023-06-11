from django import forms
from .models import pdf_file_model 

class PdfUploadForm(forms.ModelForm):

    class Meta:
        model = pdf_file_model
        fields = ['pdf_name', 'pdf_file']
        

