# coding=utf-8
# from django.template.base import Library
from django import template

register = template.Library()


@register.filter
def concat(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)

@register.filter
def get_item(dictionary, key):
    if dictionary is None:
        return ''
    if key is None:
        return dictionary
    keys = key.split('.')
    item = dictionary
    for k in keys:
        # if type(item) is not 'object':
        #     return item
        if type(item) not in [str, int]:
            item = item.get(k, '')
    return item


@register.filter
def ucwords(dictionary):
    item = dictionary
    items = item.lower() \
                .replace('_', ' ') \
                .replace('.', ' ') \
                .split(' ')
    result = ''
    for item in items:
        if len(result) > 0:
            result = result + ' '
        result = result + item.capitalize()
    return result

@register.filter
def capitalize(dictionary):
    return dictionary.capitalize()

@register.filter
def lower(dictionary):
    return dictionary.lower()

@register.filter
def upper(dictionary):
    return dictionary.upper()
