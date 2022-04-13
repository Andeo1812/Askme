from django import template

register = template.Library()


@register.filter('is_newline')
def is_newline(value):
    if value % 3 == 0:
        return True
    return False
