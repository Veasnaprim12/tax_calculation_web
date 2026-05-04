"""
Currency Utilities Module

This module contains currency conversion utilities and symbols.
Easy to modify exchange rates and add new currencies.
"""

from decimal import Decimal


# Exchange rates (approximate, update as needed)
USD_TO_KHR_RATE = Decimal('4100')  # 1 USD = 4100 KHR


def convert_to_khr(amount, currency):
    """
    Convert amount to Cambodian Riel (KHR) for calculations.
    Current exchange rate: 1 USD = 4100 KHR (approximate)
    """
    if currency == 'USD':
        return amount * USD_TO_KHR_RATE
    return amount


def convert_from_khr(amount_khr, currency):
    """
    Convert amount from Cambodian Riel (KHR) to selected currency.
    """
    if currency == 'USD':
        return amount_khr / USD_TO_KHR_RATE
    return amount_khr


def get_currency_symbol(currency):
    """
    Get currency symbol for display.
    """
    if currency == 'USD':
        return '$'
    return '៛'


def get_exchange_rate(currency):
    """
    Get exchange rate to KHR.
    """
    if currency == 'USD':
        return USD_TO_KHR_RATE
    return Decimal('1')