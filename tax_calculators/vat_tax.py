"""
VAT Tax Calculator Module

This module contains all VAT tax calculation logic for Cambodia.
Easy to modify VAT rates and formulas.
"""

from decimal import Decimal


def calculate_vat_tax(amount, vat_rate):
    """
    Calculate VAT tax for a given amount and rate.

    Args:
        amount (Decimal): The amount of goods/services
        vat_rate (Decimal): The VAT rate (e.g., 0.10 for 10%)

    Returns:
        Decimal: The calculated VAT tax amount
    """
    return amount * vat_rate


def calculate_vat_tax_with_breakdown(amount, vat_rate):
    """
    Calculate VAT tax with detailed breakdown.

    Args:
        amount (Decimal): The amount of goods/services
        vat_rate (Decimal): The VAT rate (e.g., 0.10 for 10%)

    Returns:
        tuple: (tax_amount, vat_rate_percentage, total_amount)
    """
    tax_amount = calculate_vat_tax(amount, vat_rate)
    vat_rate_percentage = vat_rate * 100
    total_amount = amount + tax_amount

    return tax_amount, vat_rate_percentage, total_amount