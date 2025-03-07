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
    
    
@register.filter
def convert_to_arabic_numbers(value):
    arabic_digits = {
        '0': '٠', '1': '١', '2': '٢', '3': '٣', '4': '٤',
        '5': '٥', '6': '٦', '7': '٧', '8': '٨', '9': '٩'
    }
    if isinstance(value, str):  # If value is a string (e.g., numbers in text)
        return ''.join(arabic_digits.get(digit, digit) for digit in value)
    elif isinstance(value, int):  # If value is an integer
        return ''.join(arabic_digits.get(digit, digit) for digit in str(value))
    return value



@register.filter
def format_department(department):
    mapping = {
        "فريق الموسيقي": "موسيقي",
        "شئون الأفراد": "افراد",
        "الخدمات المعاونة": "معاونة",
        "شئون المالية": "ماليه",
        "شئون الدارسين": "دارسين",
        "شئون المجندين": "مجندين",
        "شئون الضباط": "ضباط",
    }
    # إذا كان القسم موجودًا، قم بإرجاع القيمة المختصرة من mapping أو الاسم الأصلي إذا لم يكن موجودًا في القاموس
    return mapping.get(department.name, department.name) if department else "-"


@register.filter
def format_ope(ope):
    mapping = {
        "عمل يومي": "يومي",
    }
    return mapping.get(ope, ope)



@register.filter
def format_state(state):
    mapping = {
        "نوبتجي": "🇴✓",
        "طارئة": "⚠",
        "8 صباحاً": "☼",
        "يومي": "✓",
        "مأمورية خ": "♫",
        "مأمورية": "♫",
        "انتداب": "⇄",
        "دورية": "☕︎",
        "راحة": "🏠︎",
        "ر بديلة": "🏠︎",
        "فرقة": "💡",
    }
    return mapping.get(state, state)




@register.filter(name='subtract')
def subtract(value, arg):
    """Subtracts the arg from the value, ensuring the result is not negative."""
    return max(value - arg, 0)
