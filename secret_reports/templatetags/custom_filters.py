from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    يرجع القيمة من القاموس (dictionary) حسب المفتاح (key)
    """
    try:
        return dictionary.get(key, "")
    except Exception:
        return ""

@register.filter
def index(sequence, position):
    """
    يعيد العنصر من القائمة في الموضع المحدد (position)
    إذا كانت القيمة غير صحيحة أو الفهرس خارج النطاق يعيد قيمة فارغة
    """
    try:
        position = int(position)
        return sequence[position]
    except (IndexError, ValueError, TypeError):
        return ''

@register.filter
def first(value):
    """
    يعيد أول عنصر من قائمة أو Tuple
    """
    try:
        return value[0]
    except (IndexError, TypeError):
        return ''

@register.filter
def slice(value, arg):
    """
    فلتر بديل للتقطيع مثل [start:end]
    يُستخدم كـ {{ value|slice:"1:2" }}
    """
    try:
        start, end = map(int, arg.split(':'))
        return value[start:end]
    except Exception:
        return value
