

from django import template

register = template.Library()

@register.filter
def get_field_value(employee, field_name):
    return getattr(employee, field_name, None)

@register.filter
def make_range(value):
    start, end = map(int, value.split())
    return range(start, end + 1)

@register.filter
def make_list(value):
    return range(1, int(value) + 1)