# this file is to create custom filters

from django import template

register = template.Library()

@register.filter
def index(sequence, position):
    try:
        return sequence[position]
    except:
        return None
