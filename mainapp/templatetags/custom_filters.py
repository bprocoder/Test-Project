# custom_filters.py

from django import template
register = template.Library()

@register.filter
def zip_lists(a, b):
    return zip(a, b)


# Add this to your custom_filters.py

@register.filter
def get_item(list, index):
    return list[index]
