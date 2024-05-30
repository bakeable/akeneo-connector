import locale

DefaultLocale = "nl_NL"
AkeneoUnitToSuffixByLocale = {
    "en_US": {
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
    },
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
AkeneoUnitToSuffixDefault = AkeneoUnitToSuffixByLocale[DefaultLocale]
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


def format_value(value: str | dict, locale_name: str | None = None, linked_data: dict | None = {}) -> str:
    """
    Format the value of an attribute.
    """
    if locale_name is None:
        locale_name = DefaultLocale

    if linked_data is None:
        linked_data = {}

    if value is None:
        return "N/A"
    
    if isinstance(value, str) and value.replace('.', '', 1).isdigit():
        return format_number(float(value), locale_name)
    
    if isinstance(value, int) or isinstance(value, float):
        return format_number(value, locale_name)

    if isinstance(value, str):
        if "code" in linked_data and linked_data["code"] == value:
            # Get the label from the linked data
            return linked_data.get("labels", {}).get(locale_name, value)

        return value
    

    if isinstance(value, dict):
        if 'amount' in value and 'unit' in value:
            # Get suffix for unit
            suffix = AkeneoUnitToSuffixByLocale.get(locale_name, AkeneoUnitToSuffixDefault).get(value['unit'], value['unit'])

            # Get rounding for unit
            rounding = AkeneoUnitRounding.get(value['unit'], 2)
            
            # Parse str amount to float
            amount = float(value['amount'])

            # Round value
            amount = round(amount, rounding)
            if amount.is_integer():
                amount = int(amount)
                
            # Format correctly
            formatted_amount = format_number(amount, locale_name)

            # Get the unit translation
            return f"{formatted_amount} {suffix}"
        
        if 'amount' in value and 'currency' in value:
            return f"{value['amount']} {value['currency']}"
    
    if isinstance(value, list):
        # Get labels from linked data, otherwise use the value
        labels = []
        for item in value:
            if item in linked_data:
                label = linked_data.get(item, {}).get("labels", {}).get(locale_name, item)
                labels.append(label)
            else:
                labels.append(item)

        # Add comma to all value up until the final one, 
        # then the connection word and the final value
        if len(labels) == 1:
            return labels[0]
        
        if len(labels) == 2:
            return f"{labels[0]} {ConnectionWordByLocale.get(locale_name, 'and')} {labels[1]}"
        
        return f"{', '.join(labels[:-1])} {ConnectionWordByLocale.get(locale_name, 'and')} {labels[-1]}"
    
    try:
        return str(labels)
    except:
        return "N/A"
    

def format_number(number: int | float, locale_name: str | None = None) -> str:
    if locale_name is None:
        locale_name = DefaultLocale

    try:
        # Set the locale for all categories to the specified locale
        locale.setlocale(locale.LC_ALL, locale_name)
    except locale.Error as e:
        print(f"Error setting locale to {locale_name}: {e}")
        return str(number)
    
    # Format the number
    if isinstance(number, int):
        if number > 1000000000: # Prevent barcodes from being formatted wrong
            formatted_number = str(number)
        else:
            formatted_number = locale.format_string("%d", number, grouping=True)
    else:
        formatted_number = locale.format_string("%f", number, grouping=True)

    # Remove trailing zeros, commas and dots
    formatted_number = formatted_number.rstrip('0').rstrip('.').rstrip(',')

    return formatted_number