# reports/templatetags/report_tags.py

from django import template

register = template.Library()

@register.filter(name='pluck')
def pluck(value, arg):
    """
    Extracts the attribute or dict key 'arg' from each item in 'value' (iterable).
    Usage in template: {{ data|pluck:"day" }}
    """
    result = []
    for item in value:
        if isinstance(item, dict):
            result.append(item.get(arg))
        else:
            result.append(getattr(item, arg, None))
    return result
