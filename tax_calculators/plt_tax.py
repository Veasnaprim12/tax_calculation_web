from decimal import Decimal, ROUND_HALF_UP

def calculate_plt_tax(total_sales, vat_inclusion='inclusive', vat_percentage=10):
    """
    Calculates the Public Lighting Tax (PLT) based on total sales.
    
    Parameters:
    - total_sales: The sales amount entered by the user.
    - vat_inclusion: 'inclusive' if VAT is mixed into the price, 'exclusive' if not.
    - vat_percentage: The variable VAT rate percentage (e.g., 10, 4, 0).
    
    Formula if inclusive: 
        Taxable Base = (Total Sales / (1 + VAT%)) / 1.05
    Formula if exclusive: 
        Taxable Base = Total Sales / 1.05
    """
    # Ensure all inputs are treated as Decimals for precision financial arithmetic
    total_sales = Decimal(str(total_sales))
    vat_percentage = Decimal(str(vat_percentage))
    
    # PLT standard rates
    plt_divisor = Decimal('1.05')
    plt_rate = Decimal('0.05')
    
    # 1. Determine Taxable Base based on VAT inclusion condition
    if vat_inclusion == 'inclusive':
        # Dynamically calculate the VAT divisor (e.g., 10% becomes 1.10, 4% becomes 1.04)
        vat_divisor = Decimal('1') + (vat_percentage / Decimal('100'))
        taxable_base = (total_sales / vat_divisor) / plt_divisor
    else:
        # VAT is not included, strip out only the embedded 5% PLT
        taxable_base = total_sales / plt_divisor
        
    # 2. Calculate the final 5% PLT amount
    plt_total = taxable_base * plt_rate
    
    # Round cleanly to 2 decimal places using standard financial rounding
    return plt_total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)