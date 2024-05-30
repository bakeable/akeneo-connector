AkeneoUnitToSuffixDefault = {
    'KILOGRAM': 'kg',
    'GRAM': 'g',
    'MILLIGRAM': 'mg',
    'MICROGRAM': 'µg',
    'TON': 't',
    'POUND': 'lb',
    'OUNCE': 'oz',
    'MILLIMETER': 'mm',
    'CENTIMETER': 'cm',
    'METER': 'm',
    'KILOMETER': 'km',
    'INCH': 'in',
    'FOOT': 'ft',
    'YARD': 'yd',
    'PIECE': 'pc',
    'DOZEN': 'dz',
    'MILLILITER': 'ml',
    'CENTILITER': 'cl',
    'LITER': 'l',
    'GALLON': 'gal',
    'BOX': 'box',
    'PACK': 'pack',
    'BOTTLE': 'bottle',
}
AkeneoUnitToSuffixByLocale = {
    "en_US": AkeneoUnitToSuffixDefault,
    "nl_NL": {
        'KILOGRAM': 'kg',
        'GRAM': 'g',
        'MILLIGRAM': 'mg',
        'MICROGRAM': 'µg',
        'TON': 't',
        'POUND': 'lb',
        'OUNCE': 'oz',
        'MILLIMETER': 'mm',
        'CENTIMETER': 'cm',
        'METER': 'm',
        'KILOMETER': 'km',
        'INCH': 'in',
        'FOOT': 'ft',
        'YARD': 'yd',
        'PIECE': 'stuks',
        'DOZEN': 'dz',
        'MILLILITER': 'ml',
        'CENTILITER': 'cl',
        'LITER': 'l',
        'GALLON': 'gal',
        'BOX': 'dozen',
        'PACK': 'verpakkingen',
        'BOTTLE': 'flessen',
    },
    "de_DE": {
        'KILOGRAM': 'kg',
        'GRAM': 'g',
        'MILLIGRAM': 'mg',
        'MICROGRAM': 'µg',
        'TON': 't',
        'POUND': 'lb',
        'OUNCE': 'oz',
        'MILLIMETER': 'mm',
        'CENTIMETER': 'cm',
        'METER': 'm',
        'KILOMETER': 'km',
        'INCH': 'in',
        'FOOT': 'ft',
        'YARD': 'yd',
        'PIECE': 'Stück',
        'DOZEN': 'Dutzend',
        'MILLILITER': 'ml',
        'CENTILITER': 'cl',
        'LITER': 'l',
        'GALLON': 'gal',
        'BOX': 'Karton',
        'PACK': 'Packung',
        'BOTTLE': 'Flasche',
    },
}
AkeneoUnitRounding = {
    'KILOGRAM': 2,
    'GRAM': 0,
    'MILLIGRAM': 0,
    'MICROGRAM': 0,
    'TON': 2,
    'POUND': 2,
    'OUNCE': 2,
    'MILLIMETER': 0,
    'CENTIMETER': 0,
    'METER': 2,
    'KILOMETER': 2,
    'INCH': 2,
    'FOOT': 2,
    'YARD': 2,
    'PIECE': 0,
    'DOZEN': 0,
    'MILLILITER': 0,
    'CENTILITER': 0,
    'LITER': 2,
    'GALLON': 2,
    'BOX': 0,
    'PACK': 0,
    'BOTTLE': 0,
}
ConnectionWordByLocale = {
    "en_US": "and",
    "nl_NL": "en",
    "de_DE": "und",
}


def format_value(value: str | dict, locale: str = "nl_NL") -> str:
    """
    Format the value of an attribute.
    """

    if isinstance(value, str):
        return value
    
    if 'amount' in value and 'unit' in value:
        # Get suffix for unit
        suffix = AkeneoUnitToSuffixByLocale.get(locale, AkeneoUnitToSuffixDefault).get(value['unit'], value['unit'])

        # Get rounding for unit
        rounding = AkeneoUnitRounding.get(value['unit'], 2)

        # Round value
        amount = round(value['amount'], rounding)
        if amount.is_integer():
            amount = int(value['amount'])

        # Get the unit translation
        return f"{amount} {suffix}"
    
    if 'amount' in value and 'currency' in value:
        return f"{value['amount']} {value['currency']}"
    
    if isinstance(value, list):
        # Add comma to all value up until the final one, 
        # then the connection word and the final value
        if len(value) == 1:
            return value[0]
        
        if len(value) == 2:
            return f"{value[0]} {ConnectionWordByLocale.get(locale, 'and')} {value[1]}"
        
        return f"{', '.join(value[:-1])} {ConnectionWordByLocale.get(locale, 'and')} {value[-1]}"
    
    try:
        return str(value)
    except:
        return "N/A"