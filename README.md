# Tax Calculation Web App

A Django-based web application for calculating taxes on salary and property.

## Features

- Salary tax calculation
- Property tax calculation
- Admin records management
- Responsive web interface

## Installation

1. Ensure you have Python 3.8+ installed.
2. Clone this repository:
   ```
   git clone <repository-url>
   cd tax_calculation
   ```
3. Install dependencies:
   ```
   pip install django
   ```
   (If there's a `requirements.txt`, run `pip install -r requirements.txt` instead)
4. Run database migrations:
   ```
   python manage.py migrate
   ```
5. Start the development server:
   ```
   python manage.py runserver
   ```
6. Open your browser and navigate to `http://127.0.0.1:8000/`

## Usage

- Visit the home page to select the type of tax calculation.
- Fill in the required details in the forms.
- View calculated taxes and admin records.

## Project Structure

- `calculator/`: Main app containing models, views, forms, etc.
- `tax_calculation/`: Django project settings.
- `static/`: CSS and images.
- `template/`: HTML templates.
- `db.sqlite3`: SQLite database file.

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Make your changes and test.
4. Submit a pull request.

## License

This project is licensed under the MIT License.