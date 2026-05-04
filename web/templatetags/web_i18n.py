from django import template

register = template.Library()

VALUE_KEYS = {
    "Used": "used",
    "Damaged": "damaged",
    "New": "new",
    "Stock": "stock",
    "Auction": "auction",
    "Petrol": "petrol",
    "Diesel": "diesel",
    "Electric": "electric",
    "Hybrid": "hybrid",
}


@register.filter
def translate_value(value, translations):
    key = VALUE_KEYS.get(str(value))
    if not key:
        return value
    return translations.get(key, value)
