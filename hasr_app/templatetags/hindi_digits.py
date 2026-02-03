from django import template
import datetime

register = template.Library()

@register.filter(name='to_hindi')
def to_hindi(value):
    """
    Convert numbers to Eastern Arabic (Hindi) numerals.
    Works for strings, integers, and date objects.
    """
    if value is None:
        return ""
    
    # Handle dates specifically if strictly required, but usually string conversion covers it
    # if the date format uses standard digits.
    # However, date|date:"Y/m/d" returns a string, so we just process the string.
    
    str_val = str(value)
    
    # Mapping
    replacements = {
        '0': '٠', '1': '١', '2': '٢', '3': '٣', '4': '٤',
        '5': '٥', '6': '٦', '7': '٧', '8': '٨', '9': '٩'
    }
    
    result = []
    for char in str_val:
        result.append(replacements.get(char, char))
    
    return "".join(result)
