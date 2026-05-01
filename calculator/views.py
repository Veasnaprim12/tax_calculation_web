from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from .forms import SalaryTaxForm, PropertyTaxForm
from .models import TaxRecord
from decimal import Decimal


def home(request):
    """
    Render the home page with educational content about taxes.
    """
    return render(request, "home.html")


def about_tax(request):
    """
    Render the about tax page with information about taxes.
    """
    return render(request, "about_tax.html")


def salary_tax(request):
    form = SalaryTaxForm()
    tax_amount = None
    net_income = None
    selected_currency = 'KHR'
    
    # Initialize breakdown variables
    tax_rate = None
    deduction_children = 0
    deduction_wife = 0
    grants_benefits_amount = 0
    taxable_income = None
    salary_tax = None
    grant_tax = None
    
    if request.method == 'POST':
        form = SalaryTaxForm(request.POST)
        if form.is_valid():
            currency = form.cleaned_data['currency']
            income = form.cleaned_data['income']
            status = form.cleaned_data['status']
            dependents = form.cleaned_data['dependents']
            grants_benefits = form.cleaned_data.get('grants_benefits', 0) or 0
            selected_currency = currency
            
            # Convert to KHR for calculation if needed
            income_khr = convert_to_khr(income, currency) * 12  # Annualize monthly income
            grants_benefits_khr = convert_to_khr(grants_benefits, currency) * 12  # Annualize
            
            # Calculate tax with breakdown (on annual amounts)
            tax_amount_annual_khr, tax_rate, deduction_children, deduction_wife, taxable_income_annual_khr = calculate_salary_tax_with_breakdown(
                income_khr, status, dependents, grants_benefits_khr
            )
            
            # Calculate salary tax and grant tax separately for breakdown
            salary_tax_annual_khr = Decimal('0')
            grant_tax_annual_khr = grants_benefits_khr * Decimal('0.20')
            
            # Calculate taxable income for salary (excluding grants)
            taxable_salary_annual_khr = max(Decimal('0'), income_khr - (deduction_children + deduction_wife))
            
            # Calculate salary tax using progressive system
            if taxable_salary_annual_khr > Decimal('1320000'):
                taxable_above = taxable_salary_annual_khr - Decimal('1320000')
                remaining = taxable_above
                
                # Bracket 1: 0 - 680,000 at 5%
                bracket1_limit = Decimal('680000')
                if remaining > 0:
                    bracket1_amount = min(remaining, bracket1_limit)
                    salary_tax_annual_khr += bracket1_amount * Decimal('0.05')
                    remaining -= bracket1_amount
                
                # Bracket 2: 680,001 - 7,180,000 at 10%
                bracket2_limit = Decimal('6180000')
                if remaining > 0:
                    bracket2_amount = min(remaining, bracket2_limit)
                    salary_tax_annual_khr += bracket2_amount * Decimal('0.10')
                    remaining -= bracket2_amount
                
                # Bracket 3: 7,180,001 - 11,180,000 at 15%
                bracket3_limit = Decimal('4000000')
                if remaining > 0:
                    bracket3_amount = min(remaining, bracket3_limit)
                    salary_tax_annual_khr += bracket3_amount * Decimal('0.15')
                    remaining -= bracket3_amount
                
                # Bracket 4: Over 11,180,000 at 20%
                if remaining > 0:
                    salary_tax_annual_khr += remaining * Decimal('0.20')
            
            tax_amount_khr = tax_amount_annual_khr / Decimal('12')  # Monthly tax
            salary_tax_khr = salary_tax_annual_khr / Decimal('12')  # Monthly salary tax
            grant_tax_khr = grant_tax_annual_khr / Decimal('12')  # Monthly grant tax
            net_income_khr = (income_khr / Decimal('12')) - tax_amount_khr  # Monthly net
            
            # Convert back to selected currency for display
            tax_amount = convert_from_khr(tax_amount_khr, currency)
            salary_tax = convert_from_khr(salary_tax_khr, currency)
            grant_tax = convert_from_khr(grant_tax_khr, currency)
            net_income = convert_from_khr(net_income_khr, currency)
            taxable_income = convert_from_khr(taxable_income_annual_khr / Decimal('12'), currency)  # Monthly taxable
            deduction_children = convert_from_khr(deduction_children / Decimal('12'), currency)  # Monthly
            deduction_wife = convert_from_khr(deduction_wife / Decimal('12'), currency)
            grants_benefits_amount = convert_from_khr(grants_benefits_khr / 12, currency)
            
            # Save to database in KHR
            TaxRecord.objects.create(
                tax_type='salary',
                currency=currency,
                income=income,
                status=status,
                dependents=dependents,
                tax_amount=tax_amount,
                net_income=net_income
            )
    
    return render(request, "salary_tax.html", {
        'form': form,
        'tax_amount': tax_amount,
        'net_income': net_income,
        'selected_currency': selected_currency,
        'currency_symbol': get_currency_symbol(selected_currency),
        'tax_rate': tax_rate,
        'tax_rate_percentage': tax_rate * 100 if tax_rate else None,
        'deduction_children': deduction_children,
        'deduction_wife': deduction_wife,
        'grants_benefits_amount': grants_benefits_amount,
        'taxable_income': taxable_income,
        'salary_tax': salary_tax,
        'grant_tax': grant_tax
    })


def property_tax(request):
    form = PropertyTaxForm()
    tax_amount = None
    selected_currency = 'KHR'
    
    if request.method == 'POST':
        form = PropertyTaxForm(request.POST)
        if form.is_valid():
            currency = form.cleaned_data['currency']
            property_value = form.cleaned_data['property_value']
            property_type = form.cleaned_data['property_type']
            selected_currency = currency
            
            # Convert to KHR for calculation if needed
            property_value_khr = convert_to_khr(property_value, currency)
            
            # Calculate tax
            tax_amount_khr = calculate_property_tax(property_value_khr, property_type)
            
            # Convert back to selected currency for display
            tax_amount = convert_from_khr(tax_amount_khr, currency)
            
            # Save to database
            TaxRecord.objects.create(
                tax_type='property',
                currency=currency,
                income=property_value,  # Set income to property_value for property tax
                property_value=property_value,
                property_type=property_type,
                tax_amount=tax_amount
            )
    
    return render(request, "property_tax.html", {
        'form': form,
        'tax_amount': tax_amount,
        'selected_currency': selected_currency,
        'currency_symbol': get_currency_symbol(selected_currency)
    })


@staff_member_required
def admin_records(request):
    """
    Admin-only view to see all tax calculation records.
    """
    # Get all records with filtering options
    records = TaxRecord.objects.all().order_by('-created_at')
    
    # Filter by tax type if specified
    tax_type_filter = request.GET.get('tax_type')
    if tax_type_filter:
        records = records.filter(tax_type=tax_type_filter)
    
    # Statistics
    total_records = records.count()
    salary_records = records.filter(tax_type='salary').count()
    property_records = records.filter(tax_type='property').count()
    
    # Calculate total tax collected (convert USD to KHR for total)
    total_tax_collected_khr = 0
    for record in records:
        if record.currency == 'USD':
            total_tax_collected_khr += record.tax_amount * 4100
        else:
            total_tax_collected_khr += record.tax_amount
    
    return render(request, "admin_records.html", {
        'records': records,
        'total_records': total_records,
        'salary_records': salary_records,
        'property_records': property_records,
        'total_tax_collected_khr': total_tax_collected_khr,
        'tax_type_filter': tax_type_filter,
    })


def calculate_salary_tax(income, status, dependents):
    """
    Cambodian salary tax calculation based on progressive rates.
    """
    from decimal import Decimal
    
    # Basic progressive tax rates for salary income
    if income <= Decimal('1000000'):  # 1M Riel
        tax_rate = Decimal('0')
    elif income <= Decimal('2000000'):  # 2M
        tax_rate = Decimal('0.05')
    elif income <= Decimal('5000000'):  # 5M
        tax_rate = Decimal('0.10')
    elif income <= Decimal('10000000'):  # 10M
        tax_rate = Decimal('0.15')
    else:
        tax_rate = Decimal('0.20')
    
    # Apply deductions based on status and dependents
    deduction = Decimal('0')
    if status == 'married':
        deduction += Decimal('1500000')  # Example deduction
    if status == 'family':
        deduction += Decimal('1500000') + (Decimal(dependents) * Decimal('150000'))
    
    taxable_income = max(Decimal('0'), income - deduction)
    tax = taxable_income * tax_rate
    
    return int(tax)


def calculate_salary_tax_with_breakdown(income, status, dependents, grants_benefits=0):
    """
    Cambodian salary tax calculation with detailed breakdown including grants/benefits.
    Income should be annual.
    Returns: (tax_amount, tax_rate, deduction_children, deduction_wife, taxable_income)
    """
    
    # Tax threshold for household head (no tax below 1,320,000 annual)
    tax_threshold = Decimal('1320000')
    
    # Calculate deductions (annual) - exclude grants_benefits from deductions
    deduction_children = Decimal(dependents) * Decimal('150000')  # 150,000 per child annually
    deduction_wife = Decimal('0')
    if status in ['married', 'family']:
        deduction_wife = Decimal('150000')  # 150,000 annually for housewife
    
    total_deductions = deduction_children + deduction_wife
    
    # Calculate taxable income after deductions (excluding grants/benefits)
    taxable_income = max(Decimal('0'), income - total_deductions)
    
    # Apply tax threshold (household head exemption)
    if taxable_income <= tax_threshold:
        salary_tax = Decimal('0')
    else:
        # Taxable amount above threshold
        taxable_above = taxable_income - tax_threshold
        
        # Progressive tax calculation for salary
        salary_tax = Decimal('0')
        remaining = taxable_above
        
        # Bracket 1: 0 - 680,000 (2,000,000 - 1,320,000) at 5%
        bracket1_limit = Decimal('2000000') - tax_threshold
        if remaining > 0:
            bracket1_amount = min(remaining, bracket1_limit)
            salary_tax += bracket1_amount * Decimal('0.05')
            remaining -= bracket1_amount
        
        # Bracket 2: 680,001 - 7,180,000 (8,500,000 - 2,000,000) at 10%
        bracket2_limit = Decimal('8500000') - Decimal('2000000')
        if remaining > 0:
            bracket2_amount = min(remaining, bracket2_limit)
            salary_tax += bracket2_amount * Decimal('0.10')
            remaining -= bracket2_amount
        
        # Bracket 3: 7,180,001 - 11,180,000 (12,500,000 - 8,500,000) at 15%
        bracket3_limit = Decimal('12500000') - Decimal('8500000')
        if remaining > 0:
            bracket3_amount = min(remaining, bracket3_limit)
            salary_tax += bracket3_amount * Decimal('0.15')
            remaining -= bracket3_amount
        
        # Bracket 4: Over 11,180,000 at 20%
        if remaining > 0:
            salary_tax += remaining * Decimal('0.20')
    
    # Calculate 20% tax on grants/benefits
    grant_tax = Decimal(grants_benefits) * Decimal('0.20')
    
    # Total tax
    total_tax = salary_tax + grant_tax
    
    # Determine the marginal tax rate for salary (rate of the last bracket used)
    if taxable_income <= tax_threshold:
        tax_rate = Decimal('0.05')  # Default rate
    elif taxable_above <= bracket1_limit:
        tax_rate = Decimal('0.05')
    elif taxable_above <= bracket1_limit + bracket2_limit:
        tax_rate = Decimal('0.10')
    elif taxable_above <= bracket1_limit + bracket2_limit + bracket3_limit:
        tax_rate = Decimal('0.15')
    else:
        tax_rate = Decimal('0.20')
    
    return total_tax, tax_rate, deduction_children, deduction_wife, taxable_income


def calculate_property_tax(property_value, property_type):
    """
    Cambodian property tax calculation.
    """
    from decimal import Decimal
    
    # Property tax rates based on property type and value
    base_rate = Decimal('0.001')  # 0.1% base rate
    
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
    if property_value > Decimal('100000000'):  # Over 100M
        rate *= Decimal('1.5')
    elif property_value > Decimal('50000000'):  # Over 50M
        rate *= Decimal('1.2')
    
    tax = property_value * rate
    return int(tax)


# Keep old function for backward compatibility
def calculate_tax(income, status, dependents):
    return calculate_salary_tax(income, status, dependents)


def convert_to_khr(amount, currency):
    """
    Convert amount to Cambodian Riel (KHR) for calculations.
    Current exchange rate: 1 USD = 4100 KHR (approximate)
    """
    if currency == 'USD':
        return amount * 4100
    return amount


def convert_from_khr(amount_khr, currency):
    """
    Convert amount from Cambodian Riel (KHR) to selected currency.
    """
    if currency == 'USD':
        return amount_khr / 4100
    return amount_khr


def get_currency_symbol(currency):
    """
    Get currency symbol for display.
    """
    if currency == 'USD':
        return '$'
    return '៛'
