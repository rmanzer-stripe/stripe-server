from django import template

register = template.Library()


@register.filter(name='stripe_amount')
def stripe_amount(value, currency):
    currencies = {
        'usd': {
            'transform': 1e-2,
            'dec': 2,
            'prefix': '$',
            'suffix': ''
        }
    }

    value = value * currencies.get(currency, {}).get('transform', 1)
    format_str = '{:.' + str(currencies.get(currency, {}).get('dec', 0)) + 'f}'
    format_val = format_str.format(value)

    prefix = currencies.get(currency, {}).get('prefix', '')
    suffix = currencies.get(currency, {}).get('suffix', '')

    return f'{prefix}{format_val}{suffix}'
