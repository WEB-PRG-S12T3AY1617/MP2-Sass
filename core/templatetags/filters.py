from django import template
from django.core import serializers

from posts.forms import OfferForm

register = template.Library()

@register.filter
def get_type(obj):
    return type(obj).__name__

@register.filter
def to_int(obj):
    return int(obj)

@register.filter
def get_offer_form(offer, disabled):
    if disabled:
        return OfferForm(instance=offer, sender=offer.offerFrom, receiver=offer.post.user, hidden='receiver').disable()
    else:
        return OfferForm(instance=offer, sender=offer.offerFrom, receiver=offer.post.user, hidden='receiver')

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