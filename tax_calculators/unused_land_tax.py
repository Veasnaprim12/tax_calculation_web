"""
Unused Land Tax Calculator Module

This module contains Cambodian Unused Land Tax calculation logic based on tax.md.
Unused Land Tax is collected annually at a rate of 2% on the value of land
exceeding 50,000 square meters (5 hectares).
"""

from decimal import Decimal

UNUSED_LAND_TAX_RATE = Decimal('0.02') # 2% annual rate
LAND_DEDUCTION_SQM = Decimal('50000')   # 50,000 m2 (5 hectares) exemption


def calculate_unused_land_tax(land_value_per_sqm, land_area_sqm, years_unused=1):
    """
    Calculate Cambodian Unused Land Tax.
    
    Formula:
    Tax Base = (Total Land Area - 50,000 m2) * Land Value per m2 (if area > 50,000 m2)
    Annual Tax = Tax Base * 2%
    
    Args:
        land_value_per_sqm (Decimal/float): Value of land per m2 in KHR
        land_area_sqm (Decimal/float): Total area of land in m2
        years_unused (int): Number of years the land has been unused
        
    Returns:
        tuple: (annual_tax, total_tax, breakdown_dict)
    """
    land_value_per_sqm = Decimal(str(land_value_per_sqm))
    land_area_sqm = Decimal(str(land_area_sqm))
    years_unused = int(years_unused)
    
    # Calculate taxable area (exceeding 50,000 m2)
    taxable_area = max(Decimal('0'), land_area_sqm - LAND_DEDUCTION_SQM)
    
    # Total land value
    total_land_value = land_area_sqm * land_value_per_sqm
    
    # Tax base (value of the taxable area)
    tax_base = taxable_area * land_value_per_sqm
    
    # Annual tax
    annual_tax = tax_base * UNUSED_LAND_TAX_RATE
    
    # Total tax for all years
    total_tax = annual_tax * Decimal(years_unused)
    
    breakdown = {
        'land_value_per_sqm': float(land_value_per_sqm),
        'land_area_sqm': float(land_area_sqm),
        'land_area_hectares': float(land_area_sqm / Decimal('10000')),
        'total_land_value': float(total_land_value),
        'taxable_area_sqm': float(taxable_area),
        'taxable_area_hectares': float(taxable_area / Decimal('10000')),
        'deduction_sqm': float(LAND_DEDUCTION_SQM),
        'deduction_hectares': float(LAND_DEDUCTION_SQM / Decimal('10000')),
        'tax_base': float(tax_base),
        'tax_rate': float(UNUSED_LAND_TAX_RATE),
        'tax_percentage': float(UNUSED_LAND_TAX_RATE * 100),
        'years_unused': years_unused,
        'annual_tax': float(annual_tax),
        'total_tax': float(total_tax)
    }
    
    return float(annual_tax), float(total_tax), breakdown


def calculate_unused_land_tax_progressive(land_value, land_area_sqm, years_unused=1, urban_type='rural'):
    """
    Backward-compatible wrapper function for views.py.
    Maps old parameters to the new Cambodian Unused Land Tax logic.
    """
    annual_tax, total_tax, breakdown = calculate_unused_land_tax(
        land_value_per_sqm=land_value,
        land_area_sqm=land_area_sqm,
        years_unused=years_unused
    )
    
    # Construct a progressive year-by-year breakdown list for UI compatibility
    yearly_taxes = []
    cumulative_tax = Decimal('0')
    
    for year in range(1, int(years_unused) + 1):
        cumulative_tax += Decimal(str(annual_tax))
        yearly_taxes.append({
            'year': year,
            'multiplier': 1.0,
            'annual_tax': float(annual_tax),
            'cumulative_tax': float(cumulative_tax)
        })
        
    breakdown['yearly_breakdown'] = yearly_taxes
    breakdown['total_tax'] = float(cumulative_tax)
    
    return float(cumulative_tax), breakdown
