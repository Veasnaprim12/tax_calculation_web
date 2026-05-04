"""
Salary Tax Calculator Module

This module contains all salary tax calculation logic for Cambodia.
Easy to modify tax brackets, rates, and deduction formulas.
"""

from decimal import Decimal


def calculate_salary_tax(income, status, dependents):
    """
    Cambodian salary tax calculation based on progressive rates.
    Legacy function for backward compatibility.
    Income should be monthly.
    """
    # Basic progressive tax rates for salary income (monthly brackets)
    if income <= Decimal('125000'):  # 125,000 Riel monthly (1.5M annual / 12)
        tax_rate = Decimal('0')
    elif income <= Decimal('166667'):  # 166,667 Riel monthly (2M annual / 12)
        tax_rate = Decimal('0.05')
    elif income <= Decimal('708333'):  # 708,333 Riel monthly (8.5M annual / 12)
        tax_rate = Decimal('0.10')
    elif income <= Decimal('1041667'):  # 1,041,667 Riel monthly (12.5M annual / 12)
        tax_rate = Decimal('0.15')
    else:
        tax_rate = Decimal('0.20')

    # Apply deductions based on status and dependents (monthly)
    deduction = Decimal('0')
    if status == 'married':
        deduction += Decimal('12500')  # 150,000 annual / 12
    if status == 'family':
        deduction += Decimal('12500') + (Decimal(dependents) * Decimal('1250'))  # 150,000 + dependents * 15,000 annual / 12

    taxable_income = max(Decimal('0'), income - deduction)
    tax = taxable_income * tax_rate

    return int(tax)


def calculate_salary_tax_with_breakdown(income, status, dependents, grants_benefits=0, wife_status='housework'):
    """
    Cambodian salary tax calculation with detailed breakdown including grants/benefits.
    Income should be annual.
    Returns: (tax_amount, tax_rate, deduction_children, deduction_wife, taxable_income)

    Tax brackets (annual income in KHR):
    - 0 to 1,500,000: 0%
    - 1,500,001 to 2,000,000: 5% (income × 5% - 75,000)
    - 2,000,001 to 8,500,000: 10% (income × 10% - 175,000)
    - 8,500,001 to 12,500,000: 15% (income × 15% - 600,000)
    - Over 12,500,000: 20% (income × 20% - 1,225,000)
    """

    # Calculate deductions (annual) - exclude grants_benefits from deductions
    deduction_children = Decimal(dependents) * Decimal('150000')  # 150,000 per child annually
    deduction_wife = Decimal('0')
    if status in ['married', 'family'] and wife_status == 'housework':
        deduction_wife = Decimal('150000')  # 150,000 annually for housewife

    total_deductions = deduction_children + deduction_wife

    # Calculate taxable income after deductions (excluding grants/benefits)
    taxable_income = max(Decimal('0'), income - total_deductions)

    # Apply tax brackets for salary income (annual)
    salary_tax = Decimal('0')
    tax_rate = Decimal('0')

    if taxable_income <= Decimal('1500000'):
        salary_tax = Decimal('0')
        tax_rate = Decimal('0')
    elif taxable_income <= Decimal('2000000'):
        salary_tax = (taxable_income * Decimal('0.05')) - Decimal('75000')
        tax_rate = Decimal('0.05')
    elif taxable_income <= Decimal('8500000'):
        salary_tax = (taxable_income * Decimal('0.10')) - Decimal('175000')
        tax_rate = Decimal('0.10')
    elif taxable_income <= Decimal('12500000'):
        salary_tax = (taxable_income * Decimal('0.15')) - Decimal('600000')
        tax_rate = Decimal('0.15')
    else:
        salary_tax = (taxable_income * Decimal('0.20')) - Decimal('1225000')
        tax_rate = Decimal('0.20')

    # Ensure tax is not negative
    salary_tax = max(Decimal('0'), salary_tax)

    # Calculate 20% tax on grants/benefits
    grant_tax = Decimal(grants_benefits) * Decimal('0.20')

    # Total tax
    total_tax = salary_tax + grant_tax

    return total_tax, tax_rate, deduction_children, deduction_wife, taxable_income


# Keep old function for backward compatibility
def calculate_tax(income, status, dependents):
    return calculate_salary_tax(income, status, dependents)