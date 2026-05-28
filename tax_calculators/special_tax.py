"""
Special Tax Calculator Module

This module contains Cambodian Special Tax calculation logic based on tax.md.
Special Tax applies to certain luxury, non-essential, or harmful goods and services.
"""

from decimal import Decimal

# Special Tax Rates by Category
SPECIAL_TAX_RATES = {
    'alcohol': Decimal('0.35'),
    'beer': Decimal('0.30'),
    'cigars': Decimal('0.25'),
    'cigarettes': Decimal('0.20'),
    'energy_drinks': Decimal('0.15'),
    'non_alcoholic': Decimal('0.10'),
    'plastic': Decimal('0.10'),
    'air_transport': Decimal('0.10'),
    'entertainment': Decimal('0.10'),
    'fruit_juice': Decimal('0.05'),
    'cement': Decimal('0.05'),
    'telecom': Decimal('0.03'),
    'general': Decimal('0.10') # Default fallback
}

CATEGORY_LABELS = {
    'alcohol': 'គ្រឿងស្រវឹង (Alcohol) - 35%',
    'beer': 'ស្រាបៀរ (Beer) - 30%',
    'cigars': 'បារីស៊ីហ្គា (Cigars) - 25%',
    'cigarettes': 'បារីសាមញ្ញ (Cigarettes) - 20%',
    'energy_drinks': 'ភេសជ្ជៈពៅកម្លាំង (Energy Drinks) - 15%',
    'non_alcoholic': 'ភេសជ្ជៈគ្មានជាតិអាល់កុល/ទឹកផ្អែម (Non-alcoholic Beverages) - 10%',
    'plastic': 'ផលិតផលផ្លាស្ទិក (Plastic Products) - 10%',
    'air_transport': 'សេវាដឹកជញ្ជូនអ្នកដំណើរតាមផ្លូវអាកាស (Air Transport) - 10%',
    'entertainment': 'សេវាកម្សាន្ត (Entertainment Services) - 10%',
    'fruit_juice': 'ទឹកផ្លែឈើ (Fruit Juice) - 5%',
    'cement': 'ស៊ីម៉ង់ត៍ (Cement) - 5%',
    'telecom': 'សេវាទូរគមនាគមន៍ (Telecom Services) - 3%',
    'general': 'ទូទៅ (General) - 10%'
}


def calculate_special_tax(value, category='general', supply_type='domestic'):
    """
    Calculate Cambodian Special Tax for a single item/transaction.
    
    Args:
        value (Decimal/float): Value of the transaction/supply in KHR
        category (str): The tax category from SPECIAL_TAX_RATES
        supply_type (str): 'domestic' (90% base), 'service' (100% base), or 'import' (100% base)
        
    Returns:
        tuple: (tax_amount, tax_rate, breakdown_dict)
    """
    value = Decimal(value)
    tax_rate = SPECIAL_TAX_RATES.get(category, SPECIAL_TAX_RATES['general'])
    
    # Determine the Tax Base based on supply type
    if supply_type == 'domestic':
        # For domestic goods: 90% of supply price recorded on invoice
        tax_base = value * Decimal('0.9')
        base_description = '៩០% នៃតម្លៃផ្គត់ផ្គង់ (Domestic Goods Base: 90%)'
    elif supply_type == 'service':
        # For services: 100% of service fee stated on invoice
        tax_base = value
        base_description = '១០០% នៃតម្លៃសេវាកម្ម (Service Fee Base: 100%)'
    else: # import
        # For imported goods: customs value including import duty
        tax_base = value
        base_description = 'តម្លៃគយបូករួមពន្ធនាំចូល (Customs Value + Import Duty Base: 100%)'
        
    tax_amount = tax_base * tax_rate
    
    breakdown = {
        'value': float(value),
        'category': category,
        'category_display': CATEGORY_LABELS.get(category, category),
        'supply_type': supply_type,
        'supply_type_display': {
            'domestic': 'ទំនិញក្នុងស្រុក (Domestic Goods)',
            'service': 'សេវាកម្ម (Services)',
            'import': 'ទំនិញនាំចូល (Imported Goods)'
        }.get(supply_type, supply_type),
        'base_description': base_description,
        'tax_base': float(tax_base),
        'tax_rate': float(tax_rate),
        'tax_percentage': float(tax_rate * 100),
        'tax_amount': float(tax_amount)
    }
    
    return float(tax_amount), float(tax_rate), breakdown


def calculate_special_tax_with_breakdown(transaction_value, transaction_type='general', number_of_transactions=1, supply_type='domestic'):
    """
    Calculate Cambodian Special Tax for multiple transactions/quantities.
    Matches view signature requirements.
    """
    transaction_value = Decimal(transaction_value)
    number_of_transactions = int(number_of_transactions)
    
    single_tax, tax_rate, single_breakdown = calculate_special_tax(
        value=transaction_value,
        category=transaction_type,
        supply_type=supply_type
    )
    
    total_tax = Decimal(single_tax) * Decimal(number_of_transactions)
    total_transaction_value = transaction_value * Decimal(number_of_transactions)
    total_tax_base = Decimal(single_breakdown['tax_base']) * Decimal(number_of_transactions)
    
    breakdown = {
        'transaction_type': transaction_type,
        'transaction_type_display': CATEGORY_LABELS.get(transaction_type, transaction_type),
        'single_transaction_value': float(transaction_value),
        'number_of_transactions': number_of_transactions,
        'total_transaction_value': float(total_transaction_value),
        'supply_type': supply_type,
        'supply_type_display': single_breakdown['supply_type_display'],
        'tax_base': float(total_tax_base),
        'tax_rate': tax_rate,
        'tax_percentage': float(tax_rate * 100),
        'tax_per_transaction': single_tax,
        'total_tax_amount': float(total_tax)
    }
    
    return float(total_tax), breakdown
