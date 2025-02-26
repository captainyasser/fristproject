from django import forms
from .models import Rank

class RankForm(forms.ModelForm):
    class Meta:
        model = Rank
        fields = ['name']  # اسم الدرجة فقط
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'أدخل اسم الدرجة'}),
        }
