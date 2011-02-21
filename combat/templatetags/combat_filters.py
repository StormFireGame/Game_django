from django import template

from combat.models import TYPES, INJURIES

register = template.Library()

@register.filter
def get_string_injury(value):
    return INJURIES[int(value)][1]

@register.filter
def get_string_type(value):
    return TYPES[int(value)][1]

@register.filter
def get_strike_list(value):
    return range(int(value))

@register.filter
def is_win(value, arg):
#
    return 'Win' if value == arg else ''