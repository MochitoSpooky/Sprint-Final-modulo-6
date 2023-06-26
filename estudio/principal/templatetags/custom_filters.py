from django import template

register = template.Library()

@register.filter(name='format_value')
def format_value(value):
    formatted_value = f"${value:,.0f}"
    return formatted_value