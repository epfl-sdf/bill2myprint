import re
from django import template

register = template.Library()


@register.filter(name='cutre')
def cutre(text, regex):
    return re.sub(regex, '', text)
