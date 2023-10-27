from django import template

register = template.Library()

@register.simple_tag
def subtract(value1, value2):
    return value1 - value2

@register.filter
def multiply(value, arg):
    return value * arg


@register.filter
def divide(value, arg):
    return value / arg


@register.filter
def subtract1(value, arg):
    return value - arg