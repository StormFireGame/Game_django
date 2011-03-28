from django import template

from hero.models import Hero

register = template.Library()

@register.filter
def get_string_feature(value):
    return Hero.FEATURES[value][1]

@register.filter
def minus_or_plus_give(value):
    return value if value < 0 else '+' + str(value)