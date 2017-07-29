from django import template
from django.core import serializers

register = template.Library()

@register.filter
def fieldType(field):
    return field.field.widget.__class__.__name__

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_var_type(var):
    return type(var).__name__

@register.filter
def get_form_title(var):
    if(hasattr(var, 'FORM_TITLE')):
        return var.FORM_TITLE
    else:
        return None

@register.filter
def serialize_object(var):
    return serializers.serialize('json', [var])

@register.filter
def list_len(var):
    return len(var)