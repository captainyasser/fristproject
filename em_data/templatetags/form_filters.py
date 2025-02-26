from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def attr(field, attribute_string):
    """
    Adds an HTML attribute to a form field.
    Example: {{ form.name|attr:"required" }} or {{ form.name|attr:"required,placeholder=أدخل الاسم" }}
    """
    if not hasattr(field, 'as_widget'):
        return field

    # Split attribute string into individual attributes
    attrs = {}
    for attr in attribute_string.split(','):
        if '=' in attr:
            name, value = attr.split('=', 1)
            attrs[name.strip()] = value.strip()
        else:
            attrs[attr.strip()] = True

    # Render the field with the new attributes
    return mark_safe(field.as_widget(attrs=attrs))


from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def attr(field, attribute_string):
    """
    Adds HTML attributes to a form field.
    Example: {{ form.name|attr:"required" }} or {{ form.name|attr:"required,placeholder=أدخل الاسم" }}
    """
    if not hasattr(field, 'as_widget'):
        return field

    attrs = {}
    for attr in attribute_string.split(','):
        if '=' in attr:
            name, value = attr.split('=', 1)
            attrs[name.strip()] = value.strip()
        else:
            attrs[attr.strip()] = True

    return mark_safe(field.as_widget(attrs=attrs))

@register.filter
def add_class(field, class_name):
    """
    Adds a CSS class to a form field.
    Example: {{ form.name|add_class:"form-control" }}
    """
    if not hasattr(field, 'as_widget'):
        return field

    # Get existing classes (if any) and append the new class
    existing_classes = field.field.widget.attrs.get('class', '')
    new_classes = f"{existing_classes} {class_name.strip()}".strip()
    
    # Apply the updated class attribute
    return mark_safe(field.as_widget(attrs={'class': new_classes}))