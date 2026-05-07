from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from .forms import SalaryTaxForm, PropertyTaxForm, VATTaxForm
from .models import TaxRecord, TaxCalculationDetail
from decimal import Decimal
from tax_calculators import (
    calculate_salary_tax_with_breakdown,
    calculate_property_tax,
    calculate_vat_tax,
    calculate_vat_tax_with_breakdown,
    convert_to_khr,
    convert_from_khr,
    get_currency_symbol
)


def get_tax_bracket(taxable_income):
    """Helper function to determine tax bracket for salary tax"""
    if taxable_income <= Decimal('1500000'):
        return '0%'
    elif taxable_income <= Decimal('2000000'):
        return '5%'
    elif taxable_income <= Decimal('8500000'):
        return '10%'
    elif taxable_income <= Decimal('12500000'):
        return '15%'
    else:
        return '20%'


def get_property_type_multiplier(property_type):
    """Helper function to get property type multiplier"""
    if property_type == 'house':
        return Decimal('1.0')
    elif property_type == 'land':
        return Decimal('1.2')
    elif property_type == 'apartment':
        return Decimal('0.8')
    elif property_type == 'commercial':
        return Decimal('1.5')
    else:
        return Decimal('1.0')


def get_progressive_multiplier(property_value):
    """Helper function to get progressive multiplier based on property value"""
    if property_value > Decimal('100000000'):  # Over 100M KHR
        return Decimal('1.5')
    elif property_value > Decimal('50000000'):  # Over 50M KHR
        return Decimal('1.2')
    else:
        return Decimal('1.0')


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


def about_salary_tax(request):
    """
    Render the detailed salary tax information page.
    """
    return render(request, "about_salary_tax.html")


def about_property_tax(request):
    """
    Render the detailed property tax information page.
    """
    return render(request, "about_property_tax.html")


def about_vat_tax(request):
    """
    Render the detailed VAT tax information page.
    """
    return render(request, "about_vat_tax.html")


def study_plan(request):
    """
    Render the study plan page with team member information.
    """
    return render(request, "study_plan.html")


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
            income = form.cleaned_data['income']  # Annual income
            status = form.cleaned_data['status']
            wife_status = form.cleaned_data.get('wife_status', 'housework')  # Default to housework
            dependents = form.cleaned_data['dependents']
            grants_benefits = form.cleaned_data.get('grants_benefits', 0) or 0  # Annual grants/benefits
            selected_currency = currency

            # Convert to KHR for calculation if needed
            income_khr = convert_to_khr(income, currency)
            grants_benefits_khr = convert_to_khr(grants_benefits, currency)

            # Calculate tax with breakdown (on annual amounts)
            tax_amount_khr, tax_rate, deduction_children, deduction_wife, taxable_income_khr = calculate_salary_tax_with_breakdown(
                income_khr, status, dependents, grants_benefits_khr, wife_status
            )

            # Salary tax is already included in tax_amount_khr, separate grant tax
            grant_tax_khr = grants_benefits_khr * Decimal('0.20')
            salary_tax_khr = tax_amount_khr - grant_tax_khr

            # Net income calculation (annual)
            net_income_khr = income_khr - tax_amount_khr

            # Convert back to selected currency for display
            tax_amount = convert_from_khr(tax_amount_khr, currency)
            salary_tax = convert_from_khr(salary_tax_khr, currency)
            grant_tax = convert_from_khr(grant_tax_khr, currency)
            net_income = convert_from_khr(net_income_khr, currency)
            taxable_income = convert_from_khr(taxable_income_khr, currency)
            deduction_children = convert_from_khr(deduction_children, currency)
            deduction_wife = convert_from_khr(deduction_wife, currency)
            grants_benefits_amount = convert_from_khr(grants_benefits_khr, currency)
            
            # Save to database in KHR
            tax_record = TaxRecord.objects.create(
                tax_type='salary',
                currency=currency,
                income=income,
                status=status,
                wife_status=wife_status,
                dependents=dependents,
                tax_amount=tax_amount,
                net_income=net_income
            )
            
            # Create detailed calculation breakdown
            TaxCalculationDetail.objects.create(
                tax_record=tax_record,
                tax_rate=tax_rate,
                taxable_amount=taxable_income_khr,
                deduction_children=deduction_children,  # Already in KHR
                deduction_wife=deduction_wife,  # Already in KHR
                total_deductions=deduction_children + deduction_wife,
                salary_tax_amount=salary_tax_khr,
                grant_benefit_amount=grants_benefits_khr,
                grant_tax_amount=grant_tax_khr,
                tax_components={
                    'calculation_type': 'salary_tax',
                    'annual_income_khr': float(income_khr),
                    'tax_bracket': get_tax_bracket(taxable_income_khr),
                    'effective_rate': float(tax_amount_khr / income_khr) if income_khr > 0 else 0
                }
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
            tax_record = TaxRecord.objects.create(
                tax_type='property',
                currency=currency,
                income=property_value,  # Set income to property_value for property tax
                property_value=property_value,
                property_type=property_type,
                tax_amount=tax_amount
            )
            
            # Calculate breakdown components for property tax
            base_rate = Decimal('0.001')
            property_type_multiplier = get_property_type_multiplier(property_type)
            progressive_multiplier = get_progressive_multiplier(property_value_khr)
            final_rate = base_rate * property_type_multiplier * progressive_multiplier
            
            # Create detailed calculation breakdown
            TaxCalculationDetail.objects.create(
                tax_record=tax_record,
                tax_rate=final_rate,
                taxable_amount=property_value_khr,
                base_rate=base_rate,
                property_type_multiplier=property_type_multiplier,
                progressive_multiplier=progressive_multiplier,
                final_rate=final_rate,
                tax_components={
                    'calculation_type': 'property_tax',
                    'property_value_khr': float(property_value_khr),
                    'property_type': property_type,
                    'rate_breakdown': {
                        'base_rate': float(base_rate),
                        'type_multiplier': float(property_type_multiplier),
                        'progressive_multiplier': float(progressive_multiplier),
                        'final_rate': float(final_rate)
                    }
                }
            )
    
    return render(request, "property_tax.html", {
        'form': form,
        'tax_amount': tax_amount,
        'selected_currency': selected_currency,
        'currency_symbol': get_currency_symbol(selected_currency)
    })


def vat_tax(request):
    """
    Handle VAT tax calculation form submission and display.
    """
    form = VATTaxForm()
    tax_amount = None
    total_amount = None
    selected_currency = 'KHR'

    # Initialize breakdown variables
    vat_rate = None
    vat_rate_percentage = None
    amount = None

    if request.method == 'POST':
        form = VATTaxForm(request.POST)
        if form.is_valid():
            currency = form.cleaned_data['currency']
            amount = form.cleaned_data['amount']
            vat_rate = Decimal(form.cleaned_data['vat_rate'])

            selected_currency = currency

            # Calculate VAT tax with breakdown
            tax_amount, vat_rate_percentage, total_amount = calculate_vat_tax_with_breakdown(amount, vat_rate)

            # Save to database
            tax_record = TaxRecord.objects.create(
                tax_type='vat',
                currency=currency,
                income=amount,  # Use income field for amount
                tax_amount=tax_amount
            )

            # Create detailed calculation breakdown
            TaxCalculationDetail.objects.create(
                tax_record=tax_record,
                tax_rate=vat_rate,
                taxable_amount=amount,
                tax_components={
                    'calculation_type': 'vat_tax',
                    'amount': float(amount),
                    'vat_rate': float(vat_rate),
                    'tax_amount': float(tax_amount),
                    'total_amount': float(total_amount)
                }
            )

    return render(request, "vat_tax.html", {
        'form': form,
        'tax_amount': tax_amount,
        'total_amount': total_amount,
        'amount': amount,
        'selected_currency': selected_currency,
        'currency_symbol': get_currency_symbol(selected_currency),
        'vat_rate': vat_rate,
        'vat_rate_percentage': vat_rate_percentage
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
    vat_records = records.filter(tax_type='vat').count()
    
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
        'vat_records': vat_records,
        'total_tax_collected_khr': total_tax_collected_khr,
        'tax_type_filter': tax_type_filter,
    })



