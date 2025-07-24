from django import template
register = template.Library()

@register.filter
def strval(value):
    return str(value) 