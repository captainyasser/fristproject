# yourapp/forms.py
from django import forms

class DateForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='التاريخ'  # Date label in Arabic
    )
    


class ChunkSizeForm(forms.Form):
    chunk_size = forms.IntegerField(min_value=1, label="Chunk Size")
