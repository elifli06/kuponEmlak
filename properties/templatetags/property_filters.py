from django import template

register = template.Library()


@register.filter
def price_tr(value):
    """Fiyatı Türkçe biçimde gösterir: 3400000 -> 3.400.000"""
    if value is None:
        return ''
    try:
        num = int(float(value))
        return f"{num:,}".replace(",", ".")
    except (ValueError, TypeError):
        return str(value)
