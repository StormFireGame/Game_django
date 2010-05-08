from django import template

register = template.Library()

@register.filter
def get_string_injury(value):
    INJURIES = ((0, 'Low'), (1, 'Middle'), (2, 'Top'))
    return INJURIES[int(value)][1]

@register.filter
def get_string_type(value):
    TYPES = ((0, 'Duel'), (1, 'Group'), (2, 'Chaotic'), (3, 'Territorial'))
    return TYPES[int(value)][1]