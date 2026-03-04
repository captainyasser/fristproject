# F:\emapi-edit\myproject\penalties\forms.py
from django import forms
from .models import (
    PenaltyLevel,
    PenaltyApplied,
    PenaltyAmount,
    ViolationCategory,
    ViolationType,
    ViolationPreset,
    PenaltyRecord
)

class PenaltyLevelForm(forms.ModelForm):
    class Meta:
        model = PenaltyLevel
        fields = ['name', 'is_major', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.TextInput(attrs={'class': 'form-control'}),
            'is_major': forms.CheckboxInput(),
        }


class PenaltyAppliedForm(forms.ModelForm):
    class Meta:
        model = PenaltyApplied
        fields = ['name', 'penalty_level']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'penalty_level': forms.Select(attrs={'class': 'form-control'}),
        }


from django import forms
from .models import PenaltyAmount

class PenaltyAmountForm(forms.ModelForm):
    class Meta:
        model = PenaltyAmount
        fields = ['penalty_applied', 'name', 'value', 'is_active']
        widgets = {
            'penalty_applied': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.25'}),
            'is_active': forms.CheckboxInput(),
        }



class ViolationCategoryForm(forms.ModelForm):
    class Meta:
        model = ViolationCategory
        fields = ['name']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'})}


class ViolationTypeForm(forms.ModelForm):
    class Meta:
        model = ViolationType
        fields = ['category', 'name', 'is_absence', 'description_template']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_absence': forms.CheckboxInput(),
            'description_template': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ViolationPresetForm(forms.ModelForm):
    class Meta:
        model = ViolationPreset
        fields = ['name', 'text', 'violation_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'violation_type': forms.Select(attrs={'class': 'form-control'}),
        }


class PenaltyRecordForm(forms.ModelForm):
    class Meta:
        model = PenaltyRecord
        fields = [
            'employee',
            'penalty_date',
            'category',
            'violation_type',
            'violation_description',
            'penalty_amount',
            'penalty_applied',
            'penalty_level',
            'notes',
            'form_image',
            'deduct_absence_days',
            'erase_date',
            'erase_decision_number',
            'erase_year',
            'erase_notes',
        ]
        widgets = {
            'penalty_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'erase_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'violation_description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'erase_notes': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in [
            'penalty_amount', 'notes', 'form_image',
            'erase_date', 'erase_decision_number', 'erase_year', 'erase_notes'
        ]:
            self.fields[field].required = False
