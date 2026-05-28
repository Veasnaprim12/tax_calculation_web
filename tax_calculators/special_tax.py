from decimal import Decimal

def calculate_special_tax(selling_price, product_type='spirits', product_origin='local'):
    """
    Calculate special tax according to Cambodian tax regulations.
    
    Formula for Local Products:
    Tax Base = 90% × (Selling Price / 110% / 130%)
    Special Tax = Tax Base × Tax Rate
    
    Formula for Imported Products:
    Special Tax = Import Value × Tax Rate
    
    Tax Rates:
    - Spirits/Alcohol (ស្រាវ/ម្សាធារ): 35%
    - Beer Restaurants (ម្សាធារលបៀរ): 30%
    - Spirits/Liquor (បារី): 20%
    - Karaoke Bars (បារីសីហ្គា វ): 25%
    - Furniture (ផ្គូផ្គង/ដើម): 10%
    - Silkworm Raising (សូលឺម៉ាងត្ិ៍): 5%
    - Transportation Services: 10%
    - Telecommunications: 3%
    
    Args:
        selling_price: Sale price or import value in KHR
        product_type: Type of product/service
        product_origin: 'local' or 'imported'
    
    Returns:
        Special tax amount in KHR (Decimal)
    """
    selling_price = Decimal(str(selling_price))
    
    # Define tax rates for different product types
    tax_rates = {
        'spirits': Decimal('0.35'),           # ស្រាវ/ម្សាធារ - 35%
        'beer_restaurant': Decimal('0.30'),   # ម្សាធារលបៀរ - 30%
        'liquor': Decimal('0.20'),            # បារី - 20%
        'karaoke': Decimal('0.25'),           # បារីសីហ្គា វ - 25%
        'furniture': Decimal('0.10'),         # ផ្គូផ្គង/ដើម - 10%
        'silkworm': Decimal('0.05'),          # សូលឺម៉ាងត្ិ៍ - 5%
        'transport': Decimal('0.10'),         # ដឹកជញ្ជូន - 10%
        'telecom': Decimal('0.03'),           # ទូរគមនាគមន៍ - 3%
    }
    
    # Get tax rate, default to 5% if type not specified
    tax_rate = tax_rates.get(product_type, Decimal('0.05'))
    
    # Calculate tax base based on product origin
    if product_origin == 'local':
        # Formula for local products:
        # Tax Base = 90% × (Selling Price / 110% / 130%)
        # This accounts for VAT (110%) and special tax markup (130%)
        tax_base = Decimal('0.90') * (selling_price / Decimal('1.10') / Decimal('1.30'))
    else:
        # For imported products, use the import value directly as tax base
        tax_base = selling_price
    
    # Calculate special tax amount
    special_tax_amount = tax_base * tax_rate
    
    return special_tax_amount


def get_tax_base(selling_price, product_origin='local'):
    """
    Calculate the tax base for special tax.
    
    For local products: 90% × (Selling Price / 110% / 130%)
    For imported products: Use selling price as is
    
    Args:
        selling_price: Sale price or import value
        product_origin: 'local' or 'imported'
    
    Returns:
        Tax base in KHR (Decimal)
    """
    selling_price = Decimal(str(selling_price))
    
    if product_origin == 'local':
        tax_base = Decimal('0.90') * (selling_price / Decimal('1.10') / Decimal('1.30'))
    else:
        tax_base = selling_price
    
    return tax_base


def calculate_special_tax_legacy(selling_price, product_type):
    """
    Legacy function for backward compatibility.
    Original excise tax calculation for local products.
    """
    if product_type == 'local_products':
        # Formula:
        # Excise Tax Base = 90% × (Selling Price / 110% / 130%)
        tax_base = Decimal('0.90') * (
            Decimal(selling_price) / Decimal('1.10') / Decimal('1.30')
        )
        return tax_base
    
    return Decimal('0')