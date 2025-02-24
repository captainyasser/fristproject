from django import forms
from institutes.models import Institute

class InstituteForm(forms.ModelForm):
    class Meta:
        model = Institute
        fields = ['name', 'location']
