from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter(name='ar_day')
def ar_day(value):
    # تحويل أيام الأسبوع إلى العربية
    days = {
        'Monday': 'الاثنين',
        'Tuesday': 'الثلاثاء',
        'Wednesday': 'الأربعاء',
        'Thursday': 'الخميس',
        'Friday': 'الجمعة',
        'Saturday': 'السبت',
        'Sunday': 'الأحد',
    }
    return days.get(value, value)



@register.filter(name='r_filter')  # الفلتر السابق
def r_filter(value):
    """Returns a range object for template usage."""
    try:
        return range(int(value))
    except ValueError:
        return range(0)
    
    
@register.filter(name='indexing')  # الفلتر الجديد
def indexing(sequence, position):
    """Returns the item at the given position in the sequence."""
    try:
        return sequence[position]
    except (IndexError, TypeError):
        return ""