from django import template

register = template.Library()

@register.filter(name='make_two_digit')
def make_two_digit(value):
    return f'{value:02d}'