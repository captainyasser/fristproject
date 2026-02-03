# E:\yasser\emapi2025\myproject\secret_reports\forms.py
from django import forms
from .models import SecretReport
from em_data.models import Employee

class BulkReportForm(forms.Form):
    year = forms.IntegerField(label="السنة")

    def __init__(self, *args, **kwargs):
        employees = kwargs.pop('employees')
        super().__init__(*args, **kwargs)
        for employee in employees:
            self.fields[f"score_{employee.id}"] = forms.IntegerField(
                label=employee.name, min_value=1, max_value=100, required=False
            )
