"""
Registration Tax Calculator Module

This module contains Cambodian Registration Tax calculation logic based on tax.md.
Registration Tax (4%) is imposed on the transfer of ownership of immovable property
and transportation vehicles, with specific deductions and exemptions.
"""

from decimal import Decimal

REGISTRATION_TAX_RATE = Decimal('0.04') # 4% standard rate

# Deductions for family relationships (in KHR)
INHERITANCE_DEDUCTION = Decimal('200000000') # 200 Million KHR
GIFT_DEDUCTION = Decimal('100000000')        # 100 Million KHR


def calculate_registration_tax(value, asset_type='immovable', relationship='none', is_vehicle_exempt=False):
    """
    Calculate Cambodian Registration Tax.
    
    Args:
        value (Decimal/float): Value of the asset in KHR
        asset_type (str): 'immovable' or 'vehicle'
        relationship (str): Family relationship type for immovable property:
            - 'none': Standard transfer (no deduction)
            - 'immediate_exempt': Spouse, parents, biological children, grandparents, grandchildren (100% exempt)
            - 'extended_inheritance': In-laws / Siblings inheritance (200M KHR deduction)
            - 'extended_gift': In-laws / Siblings gift (100M KHR deduction)
        is_vehicle_exempt (bool): True if motorcycle, tricycle, tractor, boat <= 150HP, etc.
        
    Returns:
        tuple: (tax_amount, tax_rate, breakdown_dict)
    """
    value = Decimal(value)
    
    if asset_type == 'immovable':
        # Immovable property calculation
        if relationship == 'immediate_exempt':
            tax_base = Decimal('0')
            tax_amount = Decimal('0')
            deduction = value
            note = "ការផ្ទេរកម្មសិទ្ធិក្នុងរង្វង់គ្រួសារផ្ទាល់ (ប្តី-ប្រពន្ធ ឪពុកម្តាយ-កូន ជីដូនជីតា-ចៅ) ត្រូវបានលើកលែងពន្ធ ១០០%។"
        elif relationship == 'extended_inheritance':
            deduction = INHERITANCE_DEDUCTION
            tax_base = max(Decimal('0'), value - deduction)
            tax_amount = tax_base * REGISTRATION_TAX_RATE
            note = "ការផ្ទេរមរតករវាងដន្លង-កូនប្រសារ ឬបងប្អូនបង្កើត ទទួលបានការកាត់កង ២០០,០០០,០០០ រៀល។"
        elif relationship == 'extended_gift':
            deduction = GIFT_DEDUCTION
            tax_base = max(Decimal('0'), value - deduction)
            tax_amount = tax_base * REGISTRATION_TAX_RATE
            note = "អំណោយលើកដំបូងរវាងដន្លង-កូនប្រសារ ឬបងប្អូនបង្កើត ទទួលបានការកាត់កង ១០០,០០០,០០០ រៀល។"
        else: # 'none'
            deduction = Decimal('0')
            tax_base = value
            tax_amount = tax_base * REGISTRATION_TAX_RATE
            note = "ការផ្ទេរកម្មសិទ្ធិទូទៅ (បង់ពន្ធ ៤% ពេញលើតម្លៃអចលនទ្រព្យ)។"
            
    else:
        # Vehicle calculation
        deduction = Decimal('0')
        if is_vehicle_exempt:
            tax_base = Decimal('0')
            tax_amount = Decimal('0')
            note = "ប្រភេទយានយន្តដែលត្រូវបានលើកលែងពន្ធ (ម៉ូតូ កង់បី ត្រាក់ទ័រ ឬកាណូត/នាវាទូក <= ១៥០ សេះ)។"
        else:
            tax_base = value
            tax_amount = tax_base * REGISTRATION_TAX_RATE
            note = "ការផ្ទេរកម្មសិទ្ធិយានយន្តទូទៅ (បង់ពន្ធ ៤% លើតម្លៃយានយន្ត)។"
            
    breakdown = {
        'value': float(value),
        'asset_type': asset_type,
        'asset_type_display': 'អចលនទ្រព្យ (Immovable Property)' if asset_type == 'immovable' else 'យានយន្ត (Vehicle)',
        'relationship': relationship,
        'relationship_display': {
            'none': 'គ្មានទំនាក់ទំនងគ្រួសារផ្ទាល់',
            'immediate_exempt': 'សាច់ញាតិផ្ទាល់ (ប្តីប្រពន្ធ/ឪពុកម្តាយកូន/ជីដូនជីតាចៅ) - លើកលែងពន្ធ',
            'extended_inheritance': 'បងប្អូនបង្កើត/ដន្លងកូនប្រសារ (មរតក - កាត់ ២០០លានរៀល)',
            'extended_gift': 'បងប្អូនបង្កើត/ដន្លងកូនប្រសារ (អំណោយ - កាត់ ១០០លានរៀល)'
        }.get(relationship, relationship),
        'is_vehicle_exempt': is_vehicle_exempt,
        'deduction': float(deduction),
        'tax_base': float(tax_base),
        'tax_rate': float(REGISTRATION_TAX_RATE),
        'tax_percentage': float(REGISTRATION_TAX_RATE * 100),
        'tax_amount': float(tax_amount),
        'note': note
    }
    
    return float(tax_amount), float(REGISTRATION_TAX_RATE), breakdown


def calculate_registration_tax_with_renewal(property_value, registration_type='property', years_renewal=0, relationship='none', is_vehicle_exempt=False):
    """
    Backward-compatible wrapper function for views.py.
    Maps old parameters to the new Cambodian Registration Tax logic.
    """
    # Map registration_type to asset_type
    asset_type = 'vehicle' if registration_type == 'vehicle' else 'immovable'
    
    tax_amount, tax_rate, breakdown = calculate_registration_tax(
        value=property_value,
        asset_type=asset_type,
        relationship=relationship,
        is_vehicle_exempt=is_vehicle_exempt
    )
    
    # Return matches views.py's expected output:
    # initial_tax, renewal_tax, total_tax, breakdown_dict
    # In Cambodia, there is no renewal fee for registration tax, so renewal_tax is 0.
    return tax_amount, 0.0, tax_amount, breakdown
