# Tax Calculation Web App

A comprehensive Django-based web application for calculating taxes on salary and property with multi-currency support and administrative record management.

## Overview

This application provides an intuitive interface for calculating income taxes and property taxes with support for different tax brackets, currency conversions, and detailed tax calculation breakdowns. It's designed for tax professionals, accountants, and individuals who need accurate tax computation.

## Features

- **Salary Tax Calculation**: Compute income tax based on salary, deductions, and tax brackets with support for spouse status
- **Property Tax Calculation**: Calculate property taxes based on property value, type, and location
- **VAT Tax Calculation**: Calculate Value Added Tax (10%) on sales with multi-currency support
- **Multi-Currency Support**: Handle tax calculations in multiple currencies (KHR, USD) with automatic conversion
- **Admin Records Management**: Store, retrieve, and manage all tax calculation records with detailed histories
- **Tax Calculation Details**: View comprehensive breakdowns of how taxes are calculated
- **Responsive Web Interface**: User-friendly design that works across desktop and mobile devices
- **Educational Information Pages**: Detailed information pages for each tax type explaining taxation rules
- **Study Plan Integration**: Educational resources about tax calculations

## Technologies Used

- **Backend**: Django 3.2+
- **Database**: SQLite3 (Development), MySQL/PostgreSQL (Production)
- **Frontend**: HTML5, CSS3
- **Language**: Python 3.8+
- **Currency**: Multi-currency support (KHR, USD)

## Installation

1. Ensure you have Python 3.8+ installed:
   ```
   python --version
   ```

2. Clone this repository:
   ```
   git clone <repository-url>
   cd tax_calculation
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
   Or manually install Django:
   ```
   pip install django
   ```

4. Run database migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser account (optional, for admin access):
   ```
   python manage.py createsuperuser
   ```

6. Start the development server:
   ```
   python manage.py runserver
   ```

7. Open your browser and navigate to `http://127.0.0.1:8000/`

## Usage

- **Home Page**: Navigate to the home page to select between salary, property, or VAT tax calculation
- **Salary Tax**: Enter your salary details, deductions, and personal information to calculate income tax
- **Property Tax**: Provide property details including value and type for property tax estimation
- **VAT Tax**: Enter your sales amount to calculate Value Added Tax (10%)
- **Information Pages**: Click the info button on each calculator to view detailed tax information
- **Admin Panel**: Access records at `/admin` using superuser credentials
- **Study Materials**: Learn about tax calculations from the study plan section

## Project Structure

```
tax_calculation/
├── calculator/                    # Main Django app
│   ├── models.py                 # Database models (TaxRecord, TaxCalculationDetail)
│   ├── views.py                  # View logic and calculations
│   ├── forms.py                  # Form definitions
│   ├── urls.py                   # URL routing
│   ├── admin.py                  # Admin interface configuration
│   ├── migrations/               # Database migrations
│   └── tests.py                  # Unit tests
├── tax_calculators/               # Calculation logic
│   ├── salary_tax.py             # Salary tax calculation algorithms
│   ├── property_tax.py           # Property tax calculation algorithms
│   ├── vat_tax.py                # VAT tax calculation algorithms
│   └── currency_utils.py         # Currency conversion utilities
├── tax_calculation/               # Django project settings
│   ├── settings.py               # Project configuration
│   ├── urls.py                   # Main URL configuration
│   ├── asgi.py                   # ASGI configuration
│   └── wsgi.py                   # WSGI configuration
├── template/                      # HTML templates
│   ├── base.html                 # Base template
│   ├── home.html                 # Home page
│   ├── salary_tax.html           # Salary tax form
│   ├── property_tax.html         # Property tax form
│   ├── vat_tax.html              # VAT tax form
│   ├── about_tax.html            # General tax information
│   ├── about_salary_tax.html     # Salary tax details
│   ├── about_property_tax.html   # Property tax details
│   ├── about_vat_tax.html        # VAT tax details
│   └── admin_records.html        # Records management
├── static/                        # Static files
│   ├── style.css                 # Stylesheet
│   └── images/                   # Images directory
└── db.sqlite3                     # SQLite database
```

## Database Models

- **TaxRecord**: Stores tax calculation records with user input and results
- **TaxCalculationDetail**: Stores detailed breakdown of tax calculations including rates and amounts

## Database Documentation

Comprehensive database documentation is available in the following files:

- **DATABASE_README.md** - Quick start guide and documentation index
- **DATABASE_DESIGN.md** - Complete schema design and architecture
- **DATABASE_SCHEMA_VISUAL.md** - Visual diagrams and references
- **DATABASE_SQL_REFERENCE.md** - SQL operations and queries
- **DATABASE_ADMIN_GUIDE.md** - Administration and operations procedures

## Tax Types and Rates

### Salary Tax
- **Progressive Rates**: 0%, 5%, 10%, 15%, 20%
- **Deductions**: Children (150K/month), Spouse (150K/month)
- **Currencies Supported**: KHR, USD

### Property Tax
- **Base Rate**: 0.1% per year
- **Multipliers**: Type-based (0.8-1.5), Value-based (1.0-1.5)
- **Currencies Supported**: KHR, USD

### VAT Tax
- **Standard Rate**: 10%
- **Calculation**: Sales Amount × 10%
- **Currencies Supported**: KHR, USD

## Testing

Run the test suite:
```
python manage.py test
```

Or use Maven (if configured):
```
mvn test
```

## Configuration

Edit `tax_calculation/settings.py` to configure:
- Database settings
- Installed apps
- Static files location
- Template directories
- Currency settings

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/amazing-feature`).
3. Make your changes and commit (`git commit -m 'Add amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.

## Troubleshooting

- **Migration errors**: Run `python manage.py migrate --fake-initial`
- **Static files not loading**: Run `python manage.py collectstatic`
- **Database locked**: Delete `db.sqlite3` and run migrations again
- **Port already in use**: Run `python manage.py runserver 8001`

## License

This project is licensed under the MIT License.