from django import template
from django.conf import settings

register = template.Library()

@register.filter
def map_position(value):
    return int(value) * -settings.ISLAND_PART_DIMENSION

@register.filter
def hero_position_up(value):
    return int(value) + 1

@register.filter
def hero_position_down(value):
    return int(value) - 1