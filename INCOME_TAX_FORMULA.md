# ​ពន្ធលើចំណូល - Income Tax Formula (Cambodia)

## Tax Brackets (ប្រាក់ចំណូលលុយប្រតិបត្តិការ)

| Taxable Profit (P) | Tax Rate | Formula |
|-------------------|----------|---------|
| ០៛ ដល់ ១៨,០០០,០០០៛ | 0% | Tax = 0 |
| ១៨,០००,००១៛ ដល់ ២៤,००००००៛ | 5% | Tax = P × 5% − 900,000 |
| ២៤,००००००១៛ ដល់ १०२,००००००៛ | 10% | Tax = P × 10% − 2,100,000 |
| १०२,००००००१៛ ដល់ १५०,००००००៛ | 15% | Tax = P × 15% − 7,200,000 |
| លលើស្ពើ ១៥០,०००,००० ៛ | 20% | Tax = P × 20% − 14,200,000 |

---

## ឧទាហរណ៍ - Examples

### ឧទាហរណ៍ ១: Income = 20,000,000 KHR
```
P = 20,000,000 KHR
This falls in bracket: 18,000,001 to 24,000,000
Tax = 20,000,000 × 5% − 900,000
Tax = 1,000,000 − 900,000
Tax = 100,000 KHR
```

### ឧទាហរណ៍ ២: Income = 50,000,000 KHR
```
P = 50,000,000 KHR
This falls in bracket: 24,000,001 to 102,000,000
Tax = 50,000,000 × 10% − 2,100,000
Tax = 5,000,000 − 2,100,000
Tax = 2,900,000 KHR
```

### ឧទាហរណ៍ ៣: Income = 120,000,000 KHR
```
P = 120,000,000 KHR
This falls in bracket: 102,000,001 to 150,000,000
Tax = 120,000,000 × 15% − 7,200,000
Tax = 18,000,000 − 7,200,000
Tax = 10,800,000 KHR
```

### ឧទាហរណ៍ ៤: Income = 200,000,000 KHR
```
P = 200,000,000 KHR
This falls in bracket: Over 150,000,000
Tax = 200,000,000 × 20% − 14,200,000
Tax = 40,000,000 − 14,200,000
Tax = 25,800,000 KHR
```

---

## Income Types (ប្រភេទចំណូល)

### 1. **Business Income (លុយប្រតិបត្តិការ)**
   - Uses progressive tax brackets above
   - Allow business expense deductions
   - Formula: `taxable_profit = income - business_expenses`

### 2. **Investment Income (ចំណូលវិនិយោគ)**
   - Fixed 20% flat tax rate
   - No deductions allowed
   - Formula: `tax = income × 20%`

### 3. **Rental Income (ឈ្នួលផ្ទះ)**
   - Fixed 20% flat tax rate
   - No deductions allowed
   - Formula: `tax = rental_amount × 20%`

### 4. **Other Income (ចំណូលផ្សេងទៀត)**
   - Fixed 20% flat tax rate
   - No deductions allowed
   - Formula: `tax = income × 20%`

---

## Calculation Steps

### For Business Income:
1. Calculate taxable profit: `Taxable Profit = Gross Income - Business Expenses`
2. Determine tax bracket based on taxable profit
3. Apply the bracket formula
4. Ensure tax is not negative: `Tax = max(0, calculated_tax)`

### For Other Income Types:
1. Apply 20% flat rate
2. Formula: `Tax = Income × 20%`

---

## Implementation (Python Code)

```python
def calculate_income_tax_with_breakdown(income, income_type='investment', business_expenses=0):
    income = Decimal(income)
    business_expenses = Decimal(business_expenses)
    
    if income_type == 'business':
        taxable_income = max(Decimal('0'), income - business_expenses)
        
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
        # Investment, Rental, Other: flat 20%
        taxable_income = income
        tax = taxable_income * Decimal('0.20')
        tax_rate = Decimal('0.20')
    
    # Ensure tax is not negative
    tax = max(Decimal('0'), tax)
    
    return tax, tax_rate, business_expenses if income_type == 'business' else Decimal('0'), taxable_income
```

---

**Note**: All calculations are based on Cambodian tax law and use KHR (Cambodian Riel) as the base currency.
