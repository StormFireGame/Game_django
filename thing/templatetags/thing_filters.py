from django import template

register = template.Library()

@register.filter
def minus_or_plus_give(value):
    return value if value < 0 else '+' + str(value) 