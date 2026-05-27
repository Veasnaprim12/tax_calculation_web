"""
Patent Tax Calculator Module

This module contains Cambodian Patent Tax calculation logic based on tax.md.
Patent Tax is an annual tax imposed on each business activity of taxpayers under
the self-assessment regime.
"""

from decimal import Decimal

# Patent Tax Rates by category
PATENT_TAX_RATES = {
    'small': Decimal('400000'),          # Small Taxpayer
    'medium': Decimal('1200000'),        # Medium Taxpayer
    'large': Decimal('3000000'),         # Large Taxpayer
    'large_above_10b': Decimal('5000000') # Large Taxpayer (Turnover > 10 Billion KHR)
}

# Minimum Patent Tax by category (for branches/warehouses in other provinces)
MINIMUM_PATENT_TAX = {
    'small': Decimal('400000'),
    'medium': Decimal('1200000'),
    'large': Decimal('3000000'),
    'large_above_10b': Decimal('3000000') # Large category minimum is 3M
}


def calculate_patent_tax(category, activities=1, timing='existing', branches=0):
    """
    Calculate Cambodian Patent Tax.
    
    Args:
        category (str): 'small', 'medium', 'large', or 'large_above_10b'
        activities (int): Number of separate business activities (each requires a patent)
        timing (str): 'existing' (full), 'new_first_half' (full), or 'new_second_half' (half)
        branches (int): Number of branches/warehouses/factories in other provinces
        
    Returns:
        tuple: (main_tax, branch_tax, total_tax, breakdown_dict)
    """
    activities = int(activities)
    branches = int(branches)
    
    # Get base rate
    base_rate = PATENT_TAX_RATES.get(category, PATENT_TAX_RATES['small'])
    
    # Get branch base rate
    branch_base_rate = MINIMUM_PATENT_TAX.get(category, MINIMUM_PATENT_TAX['small'])
    
    # Timing factor (first 6 months vs last 6 months)
    if timing == 'new_second_half':
        timing_factor = Decimal('0.5')
    else:
        timing_factor = Decimal('1.0')
        
    # Main business tax: base_rate * activities * timing_factor
    main_tax = base_rate * Decimal(activities) * timing_factor
    
    # Branch tax: branch_base_rate * branches * timing_factor
    branch_tax = branch_base_rate * Decimal(branches) * timing_factor
    
    total_tax = main_tax + branch_tax
    
    breakdown = {
        'category': category,
        'category_display': {
            'small': 'អ្នកជាប់ពន្ធតូច (Small Taxpayer)',
            'medium': 'អ្នកជាប់ពន្ធមធ្យម (Medium Taxpayer)',
            'large': 'អ្នកជាប់ពន្ធធំ (Large Taxpayer)',
            'large_above_10b': 'អ្នកជាប់ពន្ធធំ - របរលើសពី ១០ ប៊ីលានរៀល'
        }.get(category, category),
        'base_rate': float(base_rate),
        'activities': activities,
        'timing': timing,
        'timing_display': {
            'existing': 'អាជីវកម្មដែលមានស្រាប់ (បង់ពេញ)',
            'new_first_half': 'អាជីវកម្មថ្មី បង្កើតឆមាសទី១ (បង់ពេញ)',
            'new_second_half': 'អាជីវកម្មថ្មី បង្កើតឆមាសទី២ (បង់ពាក់កណ្តាល)'
        }.get(timing, timing),
        'timing_factor': float(timing_factor),
        'main_tax': float(main_tax),
        'branches': branches,
        'branch_base_rate': float(branch_base_rate),
        'branch_tax': float(branch_tax),
        'total_tax': float(total_tax)
    }
    
    return float(main_tax), float(branch_tax), float(total_tax), breakdown


def calculate_total_patent_tax(registration_type='small', action='existing', patent_term=1, renewal_years=0, current_term=0):
    """
    Backward-compatible wrapper function for the existing view and codebase.
    Maps old parameters to new Cambodian Patent Tax logic.
    
    registration_type is mapped to category.
    action is mapped to timing.
    patent_term is mapped to activities.
    renewal_years is mapped to branches.
    """
    # Map registration_type to category
    category_map = {
        'patent': 'small',
        'utility_model': 'medium',
        'design': 'large',
        'trademark': 'large_above_10b',
        'copyright': 'small',
        'small': 'small',
        'medium': 'medium',
        'large': 'large',
        'large_above_10b': 'large_above_10b'
    }
    category = category_map.get(registration_type, 'small')
    
    # Map action to timing
    timing_map = {
        'register': 'new_first_half',
        'renew': 'new_second_half',
        'register_and_renew': 'existing',
        'existing': 'existing',
        'new_first_half': 'new_first_half',
        'new_second_half': 'new_second_half'
    }
    timing = timing_map.get(action, 'existing')
    
    # Activities (patent_term) and branches (renewal_years)
    activities = max(1, patent_term)
    branches = max(0, renewal_years)
    
    main_tax, branch_tax, total_tax, breakdown = calculate_patent_tax(
        category=category,
        activities=activities,
        timing=timing,
        branches=branches
    )
    
    # Format return parameters to match what views.py expects:
    # reg_fee_khr, ren_fee_khr, total_fee_khr, breakdown_dict
    return main_tax, branch_tax, total_tax, breakdown
