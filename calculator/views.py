from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from .forms import (SalaryTaxForm, PropertyTaxForm, VATTaxForm, IncomeTaxForm, WithholdingTaxForm, PatentTaxForm,
                    SpecialTaxForm, RegistrationTaxForm, UnusedLandTaxForm, AccomodationTaxForm, PLTTaxForm, TransportationTaxForm)
from .models import TaxRecord, TaxCalculationDetail
from decimal import Decimal
from tax_calculators import (
    calculate_salary_tax_with_breakdown,
    calculate_property_tax,
    calculate_actual_vat,
    convert_to_khr,
    convert_from_khr,
    get_currency_symbol
)
from tax_calculators.income_tax import calculate_income_tax_with_breakdown
from tax_calculators.patent_tax import calculate_total_patent_tax
from tax_calculators.special_tax import calculate_special_tax_with_breakdown
from tax_calculators.registration_tax import calculate_registration_tax_with_renewal
from tax_calculators.unused_land_tax import calculate_unused_land_tax_progressive


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
def about_patent_tax(request):
    """
    Render the detailed patent tax information page.
    """
    return render(request, "about_patent.html")
def about_special_tax(request):
    """
    Render the detailed special tax information page.
    """
    return render(request, "about_special_tax.html")
def about_registration_tax(request):
    """
    Render the detailed registration tax information page.
    """
    return render(request, "about_registration_tax.html")
def about_unused_land_tax(request):
    """
    Render the detailed unused land tax information page.
    """
    return render(request, "about_unused_land.html")


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


def about_income_tax(request):
    """
    Render the detailed income tax information page.
    """
    return render(request, "about_income_tax.html")


def income_tax(request):
    """
    Render and handle the income tax calculation page.
    Income tax applies to investment, business, rental, and other non-employment income.
    """
    form = IncomeTaxForm()
    tax_amount = None
    net_income = None
    selected_currency = 'KHR'
    tax_rate = None
    taxable_income = None
    deductions = None
    
    if request.method == 'POST':
        form = IncomeTaxForm(request.POST)
        if form.is_valid():
            currency = form.cleaned_data['currency']
            income_type = form.cleaned_data['income_type']
            income = form.cleaned_data['income']
            business_expenses = form.cleaned_data.get('business_expenses', 0) or 0
            selected_currency = currency
            
            # Convert to KHR for calculation if needed
            income_khr = convert_to_khr(income, currency)
            business_expenses_khr = convert_to_khr(business_expenses, currency)
            
            # Calculate tax with breakdown
            tax_amount_khr, tax_rate, deductions_khr, taxable_income_khr = calculate_income_tax_with_breakdown(
                income_khr, income_type, business_expenses_khr
            )
            
            # Net income calculation
            net_income_khr = income_khr - tax_amount_khr
            
            # Convert back to selected currency for display
            tax_amount = convert_from_khr(tax_amount_khr, currency)
            net_income = convert_from_khr(net_income_khr, currency)
            taxable_income = convert_from_khr(taxable_income_khr, currency)
            deductions = convert_from_khr(deductions_khr, currency)
            
            # Save to database in KHR
            tax_record = TaxRecord.objects.create(
                tax_type='income',
                currency=currency,
                income=income,
                tax_amount=tax_amount,
                net_income=net_income
            )
            
            # Create detailed calculation breakdown
            TaxCalculationDetail.objects.create(
                tax_record=tax_record,
                tax_rate=tax_rate,
                taxable_amount=taxable_income_khr,
                total_deductions=deductions_khr,
                tax_components={
                    'calculation_type': 'income_tax',
                    'income_type': income_type,
                    'annual_income_khr': float(income_khr),
                    'business_expenses_khr': float(business_expenses_khr),
                    'tax_rate': float(tax_rate),
                    'effective_rate': float(tax_amount_khr / income_khr) if income_khr > 0 else 0
                }
            )
    
    return render(request, "income_tax.html", {
        'form': form,
        'tax_amount': tax_amount,
        'net_income': net_income,
        'selected_currency': selected_currency,
        'currency_symbol': get_currency_symbol(selected_currency),
        'tax_rate': tax_rate,
        'tax_rate_percentage': tax_rate * 100 if tax_rate else None,
        'taxable_income': taxable_income,
        'deductions': deductions
    })


def vat_tax(request):
    """
    Render and handle the VAT tax calculation page.
    """
    form = VATTaxForm()
    tax_amount = None
    total_amount = None
    selected_currency = 'KHR'
    currency_symbol = '៛'
    
    if request.method == 'POST':
        form = VATTaxForm(request.POST)
        if form.is_valid():
            currency = form.cleaned_data['currency']
            amount = form.cleaned_data['amount']
            selected_currency = currency
            currency_symbol = get_currency_symbol(currency)
            
            # Convert to KHR for calculation if needed
            amount_khr = convert_to_khr(amount, currency)
            
            # Calculate VAT (10% in Cambodia)
            tax_amount_khr = calculate_actual_vat(amount_khr)
            
            # Total amount including VAT
            total_amount_khr = amount_khr + tax_amount_khr
            
            # Convert back to selected currency for display
            tax_amount = convert_from_khr(tax_amount_khr, currency)
            total_amount = convert_from_khr(total_amount_khr, currency)
            
            # Save to database
            tax_record = TaxRecord.objects.create(
                tax_type='vat',
                currency=currency,
                income=amount,
                tax_amount=tax_amount,
                net_income=total_amount
            )
            
            # Create detailed calculation breakdown
            TaxCalculationDetail.objects.create(
                tax_record=tax_record,
                tax_rate=Decimal('0.10'),
                taxable_amount=amount_khr,
                tax_components={
                    'calculation_type': 'vat_tax',
                    'sale_amount_khr': float(amount_khr),
                    'vat_rate': 0.10
                }
            )
    
    return render(request, "vat_tax.html", {
        'form': form,
        'tax_amount': tax_amount,
        'total_amount': total_amount,
        'selected_currency': selected_currency,
        'currency_symbol': currency_symbol
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


def withholding_tax(request):
    """
    Render and handle the withholding tax calculation page.
    Withholding tax is deducted from salary, dividends, rental income, and other sources.
    """
    form = WithholdingTaxForm()
    tax_amount = None
    net_amount = None
    selected_currency = 'KHR'
    tax_rate = None
    
    if request.method == 'POST':
        form = WithholdingTaxForm(request.POST)
        if form.is_valid():
            currency = form.cleaned_data['currency']
            withholding_type = form.cleaned_data['withholding_type']
            amount = form.cleaned_data['amount']
            selected_currency = currency
            
            # Convert to KHR for calculation if needed
            amount_khr = convert_to_khr(amount, currency)
            
            # Calculate withholding tax based on type
            if withholding_type == 'salary':
                # For salary: typically 0% to 20% based on progressive brackets
                tax_rate = Decimal('0.10')  # Standard 10% withholding on salary
            elif withholding_type == 'dividend':
                # For dividends/corporate: 10% withholding tax
                tax_rate = Decimal('0.10')
            elif withholding_type == 'rental':
                # For rental income: 10% withholding tax
                tax_rate = Decimal('0.10')
            else:
                # Other: 20% withholding tax
                tax_rate = Decimal('0.20')
            
            # Calculate withholding tax amount
            tax_amount_khr = amount_khr * tax_rate
            
            # Net amount after withholding
            net_amount_khr = amount_khr - tax_amount_khr
            
            # Convert back to selected currency for display
            tax_amount = convert_from_khr(tax_amount_khr, currency)
            net_amount = convert_from_khr(net_amount_khr, currency)
            
            # Save to database in KHR
            tax_record = TaxRecord.objects.create(
                tax_type='withholding',
                currency=currency,
                income=amount,
                tax_amount=tax_amount,
                net_income=net_amount
            )
            
            # Create detailed calculation breakdown
            TaxCalculationDetail.objects.create(
                tax_record=tax_record,
                tax_rate=tax_rate,
                taxable_amount=amount_khr,
                tax_components={
                    'calculation_type': 'withholding_tax',
                    'withholding_type': withholding_type,
                    'amount_khr': float(amount_khr),
                    'tax_rate': float(tax_rate),
                }
            )
    
    return render(request, "withholding_tax.html", {
        'form': form,
        'tax_amount': tax_amount,
        'net_amount': net_amount,
        'selected_currency': selected_currency,
        'currency_symbol': get_currency_symbol(selected_currency),
        'tax_rate': tax_rate,
        'amount': amount if form.is_bound else None
        
    })


def about_withholding_tax(request):
    """
    Display information about withholding tax.
    """
    return render(request, "about_withholding_tax.html", {
        'title': 'ពន្ធកាត់ទុក'
    })


def patent_tax(request):
    """
    Render and handle the patent tax calculation page.
    """
    form = PatentTaxForm()
    main_tax = None
    branch_tax = None
    total_tax = None
    breakdown = None
    selected_currency = 'KHR'
    
    if request.method == 'POST':
        form = PatentTaxForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            activities = form.cleaned_data['activities']
            timing = form.cleaned_data['timing']
            branches = form.cleaned_data['branches']
            
            # Calculate patent tax using import from tax_calculators
            from tax_calculators.patent_tax import calculate_patent_tax
            main_tax_khr, branch_tax_khr, total_tax_khr, breakdown_dict = calculate_patent_tax(
                category, activities, timing, branches
            )
            
            main_tax = main_tax_khr
            branch_tax = branch_tax_khr
            total_tax = total_tax_khr
            breakdown = breakdown_dict
            
            # Save to database (income is total_tax for patent tax)
            tax_record = TaxRecord.objects.create(
                tax_type='patent',
                currency='KHR',
                income=Decimal(total_tax_khr),
                tax_amount=Decimal(total_tax_khr)
            )
            
            # Create detailed calculation breakdown
            TaxCalculationDetail.objects.create(
                tax_record=tax_record,
                tax_rate=Decimal('0'),
                taxable_amount=Decimal(total_tax_khr),
                tax_components=breakdown_dict
            )
            
    return render(request, "patent_tax.html", {
        'form': form,
        'main_tax': main_tax,
        'branch_tax': branch_tax,
        'total_tax': total_tax,
        'breakdown': breakdown,
        'selected_currency': selected_currency,
        'currency_symbol': get_currency_symbol(selected_currency),
    })


def special_tax(request):
    """
    Render and handle the special tax calculation page.
    """
    form = SpecialTaxForm()
    tax_amount = None
    total_tax = None
    breakdown = None
    selected_currency = 'KHR'
    currency_symbol = '៛'
    
    if request.method == 'POST':
        form = SpecialTaxForm(request.POST)
        if form.is_valid():
            currency = form.cleaned_data['currency']
            transaction_value = form.cleaned_data['transaction_value']
            transaction_type = form.cleaned_data['transaction_type']
            supply_type = form.cleaned_data['supply_type']
            number_of_transactions = form.cleaned_data['number_of_transactions']
            selected_currency = currency
            currency_symbol = get_currency_symbol(currency)
            
            # Convert value to KHR for calculation
            value_khr = convert_to_khr(transaction_value, currency)
            
            from tax_calculators.special_tax import calculate_special_tax_with_breakdown
            total_tax_khr, breakdown_dict = calculate_special_tax_with_breakdown(
                value_khr, transaction_type, number_of_transactions, supply_type
            )
            
            # Convert back to selected currency for display
            tax_amount = convert_from_khr(Decimal(str(breakdown_dict['tax_per_transaction'])), currency)
            total_tax = convert_from_khr(Decimal(str(total_tax_khr)), currency)
            
            # Save to database
            tax_record = TaxRecord.objects.create(
                tax_type='special',
                currency=currency,
                income=transaction_value,
                tax_amount=total_tax
            )
            
            # Create detailed calculation breakdown
            TaxCalculationDetail.objects.create(
                tax_record=tax_record,
                tax_rate=Decimal(str(breakdown_dict['tax_rate'])),
                taxable_amount=convert_to_khr(transaction_value, currency),
                tax_components=breakdown_dict
            )
            
    return render(request, "special_tax.html", {
        'form': form,
        'tax_amount': tax_amount,
        'total_tax': total_tax,
        'breakdown': breakdown,
        'selected_currency': selected_currency,
        'currency_symbol': currency_symbol,
    })


def registration_tax(request):
    """
    Render and handle the registration tax calculation page.
    """
    form = RegistrationTaxForm()
    total_tax = None
    breakdown = None
    selected_currency = 'KHR'
    currency_symbol = '៛'
    
    if request.method == 'POST':
        form = RegistrationTaxForm(request.POST)
        if form.is_valid():
            currency = form.cleaned_data['currency']
            asset_type = form.cleaned_data['asset_type']
            property_value = form.cleaned_data['property_value']
            relationship = form.cleaned_data.get('relationship', 'none')
            is_vehicle_exempt = form.cleaned_data.get('is_vehicle_exempt', False)
            selected_currency = currency
            currency_symbol = get_currency_symbol(currency)
            
            # Convert to KHR for calculation
            value_khr = convert_to_khr(property_value, currency)
            
            from tax_calculators.registration_tax import calculate_registration_tax
            tax_amount_khr, tax_rate, breakdown_dict = calculate_registration_tax(
                value_khr, asset_type, relationship, is_vehicle_exempt
            )
            
            # Convert back to selected currency for display
            total_tax = convert_from_khr(Decimal(str(tax_amount_khr)), currency)
            breakdown = breakdown_dict
            
            # Save to database
            tax_record = TaxRecord.objects.create(
                tax_type='registration',
                currency=currency,
                income=property_value,
                tax_amount=total_tax
            )
            
            # Create detailed calculation breakdown
            TaxCalculationDetail.objects.create(
                tax_record=tax_record,
                tax_rate=Decimal(str(tax_rate)),
                taxable_amount=value_khr,
                tax_components=breakdown_dict
            )
            
    return render(request, "registration_tax.html", {
        'form': form,
        'total_tax': total_tax,
        'breakdown': breakdown,
        'selected_currency': selected_currency,
        'currency_symbol': currency_symbol,
    })


def unused_land_tax(request):
    """
    Render and handle the unused land tax calculation page.
    """
    form = UnusedLandTaxForm()
    annual_tax = None
    total_tax = None
    breakdown = None
    yearly_breakdown = None
    selected_currency = 'KHR'
    currency_symbol = '៛'
    
    if request.method == 'POST':
        form = UnusedLandTaxForm(request.POST)
        if form.is_valid():
            currency = form.cleaned_data['currency']
            land_area_sqm = form.cleaned_data['land_area_sqm']
            land_value = form.cleaned_data['land_value']
            years_unused = form.cleaned_data['years_unused']
            selected_currency = currency
            currency_symbol = get_currency_symbol(currency)
            
            # Convert land value per sqm to KHR if currency is USD
            land_value_khr = convert_to_khr(land_value, currency)
            
            from tax_calculators.unused_land_tax import calculate_unused_land_tax
            annual_tax_khr, total_tax_khr, breakdown_dict = calculate_unused_land_tax(
                land_value_khr, land_area_sqm, years_unused
            )
            
            # Convert back to selected currency for display
            annual_tax = convert_from_khr(Decimal(str(annual_tax_khr)), currency)
            total_tax = convert_from_khr(Decimal(str(total_tax_khr)), currency)
            breakdown = breakdown_dict
            
            # Construct a progressive year-by-year breakdown list for UI
            yearly_taxes = []
            cumulative_tax = Decimal('0')
            for year in range(1, int(years_unused) + 1):
                cumulative_tax += Decimal(str(annual_tax))
                yearly_taxes.append({
                    'year': year,
                    'annual_tax': float(annual_tax),
                    'cumulative_tax': float(cumulative_tax)
                })
            yearly_breakdown = yearly_taxes
            
            # Save to database
            tax_record = TaxRecord.objects.create(
                tax_type='unused_land',
                currency=currency,
                income=land_value * land_area_sqm,
                tax_amount=total_tax
            )
            
            # Create detailed calculation breakdown
            TaxCalculationDetail.objects.create(
                tax_record=tax_record,
                tax_rate=Decimal('0.02'),
                taxable_amount=convert_to_khr(Decimal(str(breakdown_dict['tax_base'])), currency),
                tax_components=breakdown_dict
            )
            
    return render(request, "unused_land_tax.html", {
        'form': form,
        'annual_tax': annual_tax,
        'total_tax': total_tax,
        'breakdown': breakdown,
        'yearly_breakdown': yearly_breakdown,
        'selected_currency': selected_currency,
        'currency_symbol': currency_symbol,
    })

def about_accomodation_tax(request):
    """
    Render the detailed accommodation tax information page.
    """
    return render(request, "about_accomodation_tax.html")

def accomodation_tax(request):
    """
    Render and handle the accommodation tax calculation page.
    Accommodation tax applies to hotels, guesthouses, and similar establishments.
    """
    form = AccomodationTaxForm()
    tax_amount = None
    total_amount = None
    selected_currency = 'KHR'
    currency_symbol = '៛'
    
    if request.method == 'POST':
        form = AccomodationTaxForm(request.POST)
        if form.is_valid():
            currency = form.cleaned_data['currency']
            room_rate = form.cleaned_data['room_rate']
            nights = form.cleaned_data['nights']
            selected_currency = currency
            currency_symbol = get_currency_symbol(currency)
            
            # Convert to KHR for calculation if needed
            room_rate_khr = convert_to_khr(room_rate, currency)
            
            # Calculate accommodation tax (5% of room rate per night)
            tax_amount_khr = room_rate_khr * Decimal('0.05') * nights
            
            # Total amount including tax
            total_amount_khr = (room_rate_khr * nights) + tax_amount_khr
            
            # Convert back to selected currency for display
            tax_amount = convert_from_khr(tax_amount_khr, currency)
            total_amount = convert_from_khr(total_amount_khr, currency)
            
            # Save to database in KHR
            tax_record = TaxRecord.objects.create(
                tax_type='accomodation',
                currency=currency,
                income=room_rate * nights,
                tax_amount=tax_amount,
                net_income=total_amount
            )
    
    return render(request, "accomodation_tax.html", {
        'form': form,
        'tax_amount': tax_amount,
        'total_amount': total_amount,
        'selected_currency': selected_currency,
        'currency_symbol': currency_symbol,
    })
def about_plt_tax(request):
    """
    Render the detailed PLT tax information page.
    """
    return render(request, "about_plt_tax.html")

def plt_tax(request):
    """
    Render and handle the PLT tax calculation page.
    PLT (Public Lighting Tax) applies to alcohol and tobacco sales in Cambodia at a 5% rate.
    """
    form = PLTTaxForm()
    tax_amount = None
    selected_currency = 'KHR'
    amount = None
    
    if request.method == 'POST':
        form = PLTTaxForm(request.POST)
        if form.is_valid():
            currency = form.cleaned_data['currency']
            sales_amount = form.cleaned_data['amount'] # Matches your template and Form input property
            selected_currency = currency
            
            # Convert base values to KHR for standard engine processing
            sales_amount_khr = convert_to_khr(sales_amount, currency)
            
            # Official Cambodian PLT rate is 5%
            tax_rate = Decimal('0.05')
            tax_amount_khr = sales_amount_khr * tax_rate
            
            # Convert back to the chosen scope currency for template presentation
            tax_amount = convert_from_khr(tax_amount_khr, currency)
            amount = sales_amount
            
            # Save historical entry to TaxRecord table
            tax_record = TaxRecord.objects.create(
                tax_type='plt',
                currency=currency,
                income=sales_amount, # treating sales amount as the top-line revenue entry
                tax_amount=tax_amount
            )
            
            # Construct the breakdown logging profile safely
            TaxCalculationDetail.objects.create(
                tax_record=tax_record,
                tax_rate=tax_rate,
                taxable_amount=sales_amount_khr,
                tax_components={
                    'calculation_type': 'plt_tax',
                    'sales_amount_khr': float(sales_amount_khr),
                    'tax_amount_khr': float(tax_amount_khr),
                    'tax_rate': 0.05,
                    'effective_rate': 0.05 
                }
            )
    
    # Map the rendering symbol to cleanly match your front-end template indicators
    currency_symbol = '$' if selected_currency == 'USD' else '៛'
    
    return render(request, "plt_tax.html", {
        'form': form,
        'tax_amount': tax_amount,  
        'amount': amount,
        'currency_symbol': currency_symbol,
    })
def about_transportation_tax(request):
    """
    Render the detailed transportation tax information page.
    """
    return render(request, "about_transportation_tax.html")
    
def transportation_tax(request):
    """
    Render and handle the transportation tax calculation page.
    Transportation tax (ពន្ធផ្លូវ) applies as a flat rate based on vehicle type, 
    engine capacity (CC), and manufacture year in Cambodia.
    """
    form = TransportationTaxForm()
    tax_amount = None
    penalty_amount = Decimal('0.00')
    total_to_pay = None
    selected_currency = 'KHR' # ពន្ធផ្លូវគិតជាប្រាក់រៀលជាគោលលំនាំដើម
    
    if request.method == 'POST':
        form = TransportationTaxForm(request.POST)
        if form.is_valid():
            currency = form.cleaned_data['currency']
            vehicle_type = form.cleaned_data['vehicle_type']
            engine_capacity = form.cleaned_data['engine_capacity']   # នេះជាតម្លៃកម្លាំងម៉ាស៊ីន (CC)
            manufacture_year = form.cleaned_data['manufacture_year'] # ឆ្នាំផលិតយានជំនិះ
            is_late = form.cleaned_data.get('is_late', False)         # ស្ថានភាពបង់ប្រាក់យឺតយ៉ាវ
            
            selected_currency = currency
            
            # ១. គណនាប្រាក់ពន្ធផ្លូវជាប្រាក់រៀល (Flat rate មិនមែនលុយប្តូរតាម Currency ទេ)
            tax_amount_khr = calculate_vehicle_tax(vehicle_type, engine_capacity, manufacture_year)
            
            # ២. គណនាប្រាក់ផាកពិន័យ ១០០% ករណីហួសកាលកំណត់ (ថ្ងៃទី ៣០ កញ្ញា)
            if is_late:
                penalty_amount_khr = tax_amount_khr
            else:
                penalty_amount_khr = Decimal('0.00')
                
            total_to_pay_khr = tax_amount_khr + penalty_amount_khr
            
            # ៣. ប្រសិនបើអ្នកប្រើប្រាស់ចង់បង្ហាញជាលុយដុល្លារ (USD) ទើបបំប្លែងទឹកប្រាក់ចុងក្រោយ
            # (ចំណាំ៖ បើប្រព័ន្ធរបស់អ្នកប្រើការបំប្លែងជាមួយមុខងារ convert_from_khr)
            if currency == 'USD':
                from .utils import convert_from_khr # ឧទាហរណ៍បើមាន utility នេះ
                tax_amount = convert_from_khr(tax_amount_khr, 'USD')
                penalty_amount = convert_from_khr(penalty_amount_khr, 'USD')
                total_to_pay = convert_from_khr(total_to_pay_khr, 'USD')
            else:
                tax_amount = tax_amount_khr
                penalty_amount = penalty_amount_khr
                total_to_pay = total_to_pay_khr

            # ៤. រក្សាទុកប្រវត្តិទៅក្នុង Database (TaxRecord)
            tax_record = TaxRecord.objects.create(
                tax_type='transportation',
                currency=currency,
                income=Decimal(str(engine_capacity)),  # រក្សាទុកកម្លាំងម៉ាស៊ីនក្នុងទម្រង់លេខ Decimal
                tax_amount=total_to_pay                # ទឹកប្រាក់សរុបដែលត្រូវបង់ (រួមទាំងផាកពិន័យ បើមាន)
            )
            
            # ៥. បង្កើតកំណត់ត្រាលម្អិតសម្រាប់ប្រព័ន្ធទិន្នន័យ (TaxCalculationDetail)
            TaxCalculationDetail.objects.create(
                tax_record=tax_record,
                tax_rate=Decimal('0.00'), # ពន្ធផ្លូវមិនប្រើ % អត្រាថេរទេ ដាក់លំនាំដើម 0
                taxable_amount=Decimal(str(engine_capacity)),
                tax_components={
                    'calculation_type': 'transportation_tax',
                    'vehicle_type': vehicle_type,
                    'engine_capacity_cc': int(engine_capacity),
                    'manufacture_year': int(manufacture_year),
                    'base_tax_khr': float(tax_amount_khr),
                    'penalty_khr': float(penalty_amount_khr),
                    'total_khr': float(total_to_pay_khr),
                    'is_late_payment': is_late
                }
            )
    
    # ទាញយកនិមិត្តសញ្ញារូបិយប័ណ្ណ ($, ៛) ផ្ញើទៅកាន់ HTML Template
    currency_symbol = '$' if selected_currency == 'USD' else '៛'
    
    return render(request, "transportation_tax.html", {
        'form': form,
        'tax_amount': tax_amount,
        'penalty_amount': penalty_amount,
        'total_to_pay': total_to_pay,
        'selected_currency': selected_currency,
        'currency_symbol': currency_symbol,
    })