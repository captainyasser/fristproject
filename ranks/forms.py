from django import forms
from .models import Rank

class RankForm(forms.ModelForm):
    class Meta:
        model = Rank
        fields = ['name', 'rank_type', 'order', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم الدرجة'}),
            'rank_type': forms.Select(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'is_active': forms.Select(choices=[(True, 'نشط'), (False, 'غير نشط')], attrs={'class': 'form-control'}),
        }