from django import forms
from .models import ElawaRecord
from em_data.models import Employee
from django.forms import DateInput

class ElawaBatchForm(forms.Form):
    decision_number = forms.CharField(
        label="رقم القرار",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    elawa_date = forms.DateField(
        label="تاريخ العلاوة",
        widget=DateInput(attrs={'type':'date','class':'form-control'})
    )
    notes = forms.CharField(
        label="ملاحظات",
        required=False,
        widget=forms.Textarea(attrs={'class':'form-control','rows':3})
    )
    employees = forms.ModelMultipleChoiceField(
        queryset=Employee.objects.filter(deleted_at__isnull=True).order_by('sort_number'),
        widget=forms.CheckboxSelectMultiple(),
        required=True,
        label="اختيار الموظفين"
    )

class ElawaRecordForm(forms.ModelForm):
    class Meta:
        model = ElawaRecord
        fields = ['decision_number', 'elawa_date', 'notes']
        widgets = {
            'decision_number': forms.TextInput(attrs={'class':'form-control'}),
            'elawa_date': DateInput(attrs={'type':'date','class':'form-control'}),
            'notes': forms.Textarea(attrs={'class':'form-control','rows':3}),
        }

class MultiElawaForm(forms.Form):
    employee = forms.ModelChoiceField(
        queryset=Employee.objects.filter(deleted_at__isnull=True).order_by("sort_number"),
        label="اختر الموظف",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    # سيتم تكرار هذه الحقول في القالب
    decision_number = forms.CharField(
        label="رقم القرار",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    elawa_date = forms.DateField(
        label="تاريخ العلاوة",
        widget=DateInput(attrs={"type": "date", "class": "form-control"})
    )
    notes = forms.CharField(
        label="ملاحظات",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 2})
    )
