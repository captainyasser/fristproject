from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Custom filter to get item from dictionary using variable key.
    Usage: {{ mydict|get_item:mykey }}
    """
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return ''