from django import template

register = template.Library()


@register.filter(name='add_hyphen')
def add_hyphen(value):
    """
    Replaces blank spaces with a hyphen
    """
    return value.replace(' ', '-')




