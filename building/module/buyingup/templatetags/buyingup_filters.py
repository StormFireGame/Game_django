from django import template

register = template.Library()

@register.filter
def price_with_percent(value, arg):
    return '%.2f' % float(value * (arg / 100))