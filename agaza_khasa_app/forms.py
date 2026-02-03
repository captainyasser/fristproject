# agaza_khasa_app/forms.py
from django import forms
from .models import SpecialLeave
from django.forms.widgets import DateInput

class DateInputRtl(DateInput):
    input_type = 'date'

class SpecialLeaveForm(forms.ModelForm):
    class Meta:
        model = SpecialLeave
        fields = [
            'employee',
            'days_count',
            'duration_type',
            'leave_reason',
            'approval_date',
            'start_date',
            'return_date',
            'decision_number',
            'year',
            'notes',
        ]
        widgets = {
            'approval_date': DateInputRtl(attrs={'class': 'form-control'}),
            'start_date': DateInputRtl(attrs={'class': 'form-control'}),
            'return_date': DateInputRtl(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'employee': forms.Select(attrs={'class': 'form-select'}),
            'duration_type': forms.Select(attrs={'class': 'form-select'}),
            'leave_reason': forms.Select(attrs={'class': 'form-select'}),
            'days_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'decision_number': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class EditSpecialLeaveForm(SpecialLeaveForm):
    cut_checkbox = forms.BooleanField(required=False, label="قطع إجازة", widget=forms.CheckboxInput(attrs={'class':'form-check-input'}))
    # inherits Meta and widgets
