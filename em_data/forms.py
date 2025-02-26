from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['id_number', 'name', 'date_of_birth', 'phone_number', 'operation', 'marital_status', 'health_status', 'institute', 'rank', 'department']  # أضف الحقول التي تريد تحديثها

    def clean_id_number(self):
        id_number = self.cleaned_data['id_number']
        if id_number and Employee.objects.exclude(pk=self.instance.pk).filter(id_number=id_number).exists():
            raise forms.ValidationError("الرقم القومي موجود بالفعل.")
        return id_number