# numbers_filters.py

from django import template

register = template.Library()

@register.filter
def to_arabic_numbers(value):
    """Converts English numerals to Arabic numerals."""
    en_to_ar = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")
    return str(value).translate(en_to_ar)
