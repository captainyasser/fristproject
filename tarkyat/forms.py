from django import forms
from .models import Promotion, Employee

class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = '__all__'
        widgets = {
            'promotion_date': forms.DateInput(attrs={'type': 'date'}),
            'training_start_date': forms.DateInput(attrs={'type': 'date'}),
            'training_end_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        selected_employee_id = kwargs.pop('selected_employee_id', None)
        super(PromotionForm, self).__init__(*args, **kwargs)
        
        # ترتيب الموظفين حسب sort_number
        self.fields['employee'].queryset = Employee.objects.all().order_by('sort_number')
        self.fields['employee'].widget = forms.Select(attrs={'class': 'form-control'})
        
        # تعيين الموظف الافتراضي عند الإضافة
        if selected_employee_id and not self.instance.pk:
            try:
                self.fields['employee'].initial = Employee.objects.get(id=selected_employee_id)
            except Employee.DoesNotExist:
                pass
        
        # جعل حقل employee للقراءة فقط عند التعديل
        if self.instance and self.instance.pk:
            self.fields['employee'].widget.attrs['readonly'] = True