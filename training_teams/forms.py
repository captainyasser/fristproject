from django import forms
from .models import Places

class PlacesForm(forms.ModelForm):
    class Meta:
        model = Places
        fields = ['name', 'description', 'address']
