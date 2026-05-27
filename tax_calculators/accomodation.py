from decimal import Decimal

def calculate_accomodation_tax(property_value, property_type):
    """
    Cambodian accomodation tax calculation.

    Accomodation tax rates based on property type and value:
    - Base rate: 0.05% (0.0005)

    Adjustments by property type:
    - House: 1.0x base rate
    - Land: 1.2x base rate
    - Apartment: 0.8x base rate
    - Commercial: 1.5x base rate

    Progressive rates for high-value properties:
    - Over 100M KHR: 1.5x rate
    - Over 50M KHR: 1.2x rate
    """

    # Base rate: 0.05% = 0.0005
    base_rate = Decimal('0.0005')

    # Adjust rate based on property type
    if property_type == 'house':
        rate = base_rate * Decimal('1.0')
    elif property_type == 'land':
        rate = base_rate * Decimal('1.2')
    elif property_type == 'apartment':
        rate = base_rate * Decimal('0.8')
    elif property_type == 'commercial':
        rate = base_rate * Decimal('1.5')
    else:
        rate = base_rate

    # Progressive rates for high-value properties
    if property_value > Decimal('100000000'):  # Over 100M KHR
        rate *= Decimal('1.5')
    elif property_value > Decimal('50000000'):  # Over 50M KHR
        rate *= Decimal('1.2')

    tax = property_value * rate
    return int(tax) 
