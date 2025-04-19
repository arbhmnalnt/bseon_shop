from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """
    Adds the given CSS class(es) to a form field widget.
    Usage in template: {{ field|add_class:"form-control js-select2" }}
    """
    return field.as_widget(attrs={"class": css_class})
