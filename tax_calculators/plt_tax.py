from decimal import Decimal

def calculate_plt_tax(property_value):
    """
    Calculates the Property Land Tax (PLT) in Cambodia.
    PLT is typically 5% of the property value annually.
    """
    property_value = Decimal(str(property_value))
    plt_rate = Decimal('0.05')  # 5%
    plt_total = property_value * plt_rate
    return plt_total

