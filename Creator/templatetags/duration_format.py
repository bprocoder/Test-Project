from django import template

register = template.Library()

@register.filter
def duration_format(value):
    minutes, seconds = divmod(value.total_seconds(), 60)
    return "{} ".format(int(minutes))
    
    # return ", ".join(time_parts)