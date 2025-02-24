from django import forms
from em_data.models import Employee





class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["name", "rank", "police_number", "insurance_number", "date_of_birth"]
