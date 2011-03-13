from django import template

from combat.models import Combat

register = template.Library()

@register.filter
def get_string_injury(value):
    return Combat.INJURIES[value][1]

@register.filter
def get_string_type(value):
    return Combat.TYPES[value][1]

@register.filter
def get_strike_list(value):
    return range(int(value))

@register.filter
def is_win(value, arg):
#
    return 'Win' if value == arg else ''