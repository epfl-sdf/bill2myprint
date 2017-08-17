"""
    (c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017
"""

import locale

from django import template

register = template.Library()


@register.filter()
def format_number_abs(value):
    locale.setlocale(locale.LC_NUMERIC, '')
    return locale.format('%.2f', abs(value), True)


@register.filter()
def format_number_norm(value):
    locale.setlocale(locale.LC_NUMERIC, '')
    return locale.format('%.2f', value, True)