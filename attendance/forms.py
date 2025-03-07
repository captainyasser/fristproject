# yourapp/forms.py
from django import forms

class DateForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='التاريخ'  # Date label in Arabic
    )