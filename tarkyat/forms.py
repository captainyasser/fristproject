from django import forms
from .models import Promotion, Rank

class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = [
            'from_rank', 'to_rank', 'promotion_date', 'promotion_type', 'promotion_course_number',
            'training_start_date', 'training_end_date', 'training_course_number', 'training_location', 'notes'
        ]
        widgets = {
            'promotion_date': forms.DateInput(attrs={'type': 'date'}),
            'training_start_date': forms.DateInput(attrs={'type': 'date'}),
            'training_end_date': forms.DateInput(attrs={'type': 'date'}),
        }