# reverse string function

from django import template

register = template.Library()

@register.filter
def reverse_string(value):
    return value[::-1]
