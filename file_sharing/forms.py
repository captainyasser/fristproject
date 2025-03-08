from django import forms
from .models import SharedFile

class FileForm(forms.ModelForm):
    class Meta:
        model = SharedFile
        fields = ['file']

    # def clean_file(self):
    #     file = self.cleaned_data['file']
    #     # Example validation: limit file size to 10MB
    #     if file.size > 10 * 1024 * 1024:
    #         raise forms.ValidationError("File size must be less than 10MB.")
    #     # Add allowed file types if needed
    #     allowed_types = ['application/pdf', 'image/jpeg', 'image/png', 'text/plain']
    #     if file.content_type not in allowed_types:
    #         raise forms.ValidationError("Unsupported file type.")
    #     return file
    
    
def clean_file(self):
    file = self.cleaned_data['file']
    return file