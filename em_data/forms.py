from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        # تضمين جميع الحقول من الموديل
        fields = [
            'id_number', 'name', 'date_of_birth', 'date_of_retirement', 'age',
            'mainornot', 'sort_number', 'dep_sort', 'institute', 'image',
            'amen_or_ola', 'rank', 'rank_kind', 'nickname', 'operation',
            'police_number', 'insurance_number', 'date_of_edara', 
            'date_of_appointment', 'phone_number', 'alt_phone_number',
            'marital_status', 'gender', 'governorate', 'district', 'address',
            'health_status', 'tmamam', 'food', 'rahatcounter', 'department',
            'total_leave', 'bus', 'nots'
        ]
        
        # إعدادات إضافية لتحسين عرض الحقول في النموذج
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'date_of_retirement': forms.DateInput(attrs={'type': 'date'}),
            'date_of_edara': forms.DateInput(attrs={'type': 'date'}),
            'date_of_appointment': forms.DateInput(attrs={'type': 'date'}),
            'nots': forms.Textarea(attrs={'rows': 3}),
            'image': forms.ClearableFileInput(),
        }

    # جعل جميع الحقول اختيارية
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

    # التحقق من الرقم القومي (اختياري ولكن إذا وجد يجب أن يكون فريدًا)
    def clean_id_number(self):
        id_number = self.cleaned_data.get('id_number')
        if id_number and Employee.objects.exclude(pk=self.instance.pk).filter(id_number=id_number).exists():
            raise forms.ValidationError("الرقم القومي موجود بالفعل.")
        return id_number

    # يمكنك إضافة المزيد من التحققات حسب الحاجة
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data