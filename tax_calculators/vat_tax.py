"""
Property Tax Calculator Module

This module contains all property tax calculation logic for Cambodia.
Easy to modify tax rates, property types, and calculation formulas.
"""

from decimal import Decimal

def calculate_actual_vat(amount):
    """
    Calculates the standard 10% VAT in Cambodia.
    """
    amount = Decimal(str(amount))
    vat_rate = Decimal('0.10')
    vat_total = amount * vat_rate
    return vat_total

# Example: A $1,000 rental payment
# VAT = $100