from django import forms
from .models import SystemSetting

class SystemSettingForm(forms.ModelForm):
    class Meta:
        model = SystemSetting
        fields = ['late_notification_days']
        widgets = {
            'late_notification_days': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
