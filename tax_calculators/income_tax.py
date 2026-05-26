"""
Income Tax Calculator Module

This module contains income tax calculation logic for Cambodia.
Applies to investment income, business income, and other non-employment income.
"""

from decimal import Decimal


def calculate_income_tax_with_breakdown(income, income_type='investment', business_expenses=0):
    """
    Cambodian income tax calculation for non-employment income.
    
    Tax brackets for taxable profit (P) in KHR:
    - 0 to 18,000,000: 0%
    - 18,000,001 to 24,000,000: 5% (P×5%−900,000)
    - 24,000,001 to 102,000,000: 10% (P×10%−2,100,000)
    - 102,000,001 to 150,000,000: 15% (P×15%−7,200,000)
    - Over 150,000,000: 20% (P×20%−14,200,000)
    
    Income types:
    - investment: Dividends, interest, capital gains (20% flat rate)
    - business: Business income (progressive rates above)
    - rental: Rental income (20% flat rate)
    - other: Other income (20% flat rate)
    
    Args:
        income: Annual income in KHR
        income_type: Type of income (investment, business, rental, other)
        business_expenses: Deductible business expenses
    
    Returns: (tax_amount, tax_rate, deductions, taxable_income)
    """
    
    income = Decimal(income)
    business_expenses = Decimal(business_expenses)
    
    # Calculate taxable income after deductions
    if income_type == 'business':
        # Allow business expense deductions
        taxable_income = max(Decimal('0'), income - business_expenses)
        
        # Progressive tax brackets for business income (Cambodia tax law)
        if taxable_income <= Decimal('18000000'):
            tax = Decimal('0')
            tax_rate = Decimal('0')
        elif taxable_income <= Decimal('24000000'):
            tax = (taxable_income * Decimal('0.05')) - Decimal('900000')
            tax_rate = Decimal('0.05')
        elif taxable_income <= Decimal('102000000'):
            tax = (taxable_income * Decimal('0.10')) - Decimal('2100000')
            tax_rate = Decimal('0.10')
        elif taxable_income <= Decimal('150000000'):
            tax = (taxable_income * Decimal('0.15')) - Decimal('7200000')
            tax_rate = Decimal('0.15')
        else:
            tax = (taxable_income * Decimal('0.20')) - Decimal('14200000')
            tax_rate = Decimal('0.20')
    else:
        # Fixed 20% rate for investment, rental, and other income
        taxable_income = income
        tax = taxable_income * Decimal('0.20')
        tax_rate = Decimal('0.20')
    
    # Ensure tax is not negative
    tax = max(Decimal('0'), tax)
    
    return tax, tax_rate, business_expenses if income_type == 'business' else Decimal('0'), taxable_income


def calculate_combined_income_tax(salary_income=0, investment_income=0, business_income=0, 
                                   rental_income=0, other_income=0, business_expenses=0,
                                   status='single', dependents=0, wife_status='housework'):
    """
    Calculate combined income tax on multiple income sources.
    
    Args:
        salary_income: Salary/employment income (KHR)
        investment_income: Investment/dividend income (KHR)
        business_income: Business income (KHR)
        rental_income: Rental income (KHR)
        other_income: Other income (KHR)
        business_expenses: Deductible business expenses (KHR)
        status: Marital status (single, married, family)
        dependents: Number of dependents
        wife_status: Wife status (housework, working)
    
    Returns: (total_tax, tax_breakdown_dict, total_income, net_income)
    """
    
    salary_income = Decimal(salary_income)
    investment_income = Decimal(investment_income)
    business_income = Decimal(business_income)
    rental_income = Decimal(rental_income)
    other_income = Decimal(other_income)
    business_expenses = Decimal(business_expenses)
    dependents = int(dependents)
    
    total_income = salary_income + investment_income + business_income + rental_income + other_income
    
    # Calculate salary tax if applicable
    salary_tax = Decimal('0')
    if salary_income > 0:
        # Import here to avoid circular imports
        from salary_tax import calculate_salary_tax_with_breakdown
        salary_tax, _, _, _, _ = calculate_salary_tax_with_breakdown(
            salary_income, status, dependents, 0, wife_status
        )
    
    # Calculate investment tax (20% flat)
    investment_tax = investment_income * Decimal('0.20')
    
    # Calculate business tax (progressive or flat 20%)
    business_tax = Decimal('0')
    if business_income > 0:
        taxable_business = max(Decimal('0'), business_income - business_expenses)
        
        if taxable_business <= Decimal('1500000'):
            business_tax = Decimal('0')
        elif taxable_business <= Decimal('2000000'):
            business_tax = (taxable_business * Decimal('0.05')) - Decimal('75000')
        elif taxable_business <= Decimal('8500000'):
            business_tax = (taxable_business * Decimal('0.10')) - Decimal('175000')
        elif taxable_business <= Decimal('12500000'):
            business_tax = (taxable_business * Decimal('0.15')) - Decimal('600000')
        else:
            business_tax = (taxable_business * Decimal('0.20')) - Decimal('1225000')
        
        business_tax = max(Decimal('0'), business_tax)
    
    # Calculate rental tax (20% flat)
    rental_tax = rental_income * Decimal('0.20')
    
    # Calculate other income tax (20% flat)
    other_tax = other_income * Decimal('0.20')
    
    # Total tax
    total_tax = salary_tax + investment_tax + business_tax + rental_tax + other_tax
    net_income = total_income - total_tax
    
    # Tax breakdown
    tax_breakdown = {
        'salary_tax': salary_tax,
        'investment_tax': investment_tax,
        'business_tax': business_tax,
        'rental_tax': rental_tax,
        'other_tax': other_tax,
        'total_tax': total_tax,
    }
    
    return total_tax, tax_breakdown, total_income, net_income
