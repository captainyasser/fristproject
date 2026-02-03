from django import forms
from .models import Education
from django.forms.widgets import ClearableFileInput

class EducationForm(forms.ModelForm):
    obtained_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), required=False)
    class Meta:
        model = Education
        fields = [
            'employee',
            'decision_number',
            'university_name',
            'level',
            'qualification_type',
            'grade',
            'obtained_date',
            'degree_validation_image',
            'degree_image',
            'ministry_approval_image',
            'notes',
        ]
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-select'}),
            'decision_number': forms.TextInput(attrs={'class': 'form-control'}),
            'university_name': forms.TextInput(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-select'}),
            'qualification_type': forms.Select(attrs={'class': 'form-select'}),
            'grade': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows':3}),
            'degree_validation_image': ClearableFileInput(attrs={'class':'form-control'}),
            'degree_image': ClearableFileInput(attrs={'class':'form-control'}),
            'ministry_approval_image': ClearableFileInput(attrs={'class':'form-control'}),
        }
