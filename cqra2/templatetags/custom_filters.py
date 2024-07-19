from django import template

register = template.Library()

@register.filter
def percentage(value):
    """Converts a decimal number to a percentage string."""
    try:
        return f'{float(value) * 100:.2f}%'
    except (ValueError, TypeError):
        return ''