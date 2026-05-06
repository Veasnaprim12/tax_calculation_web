# Database Schema - Visual Reference

## Complete Database Architecture

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                     TAX CALCULATION SYSTEM DATABASE                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────────────┐
│                          📋 TAXRECORD TABLE                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  🔑 id (INTEGER, PRIMARY KEY)                                             │
│  ├─ Unique identifier for each tax record                                 │
│  └─ Auto-incrementing                                                     │
│                                                                             │
│  📁 tax_type (VARCHAR(10), NOT NULL)                                       │
│  ├─ Choices: 'salary', 'property', 'vat'                                  │
│  ├─ Index: Yes                                                             │
│  └─ Used for filtering and categorization                                 │
│                                                                             │
│  💱 currency (VARCHAR(3), DEFAULT='KHR')                                   │
│  ├─ Choices: 'KHR', 'USD'                                                 │
│  ├─ Index: Yes                                                             │
│  └─ Exchange rate: 1 USD = ~4100 KHR                                      │
│                                                                             │
│  💰 income (DECIMAL(15,2), NOT NULL)                                       │
│  ├─ Salary amount, Property value, or Sales amount                        │
│  ├─ Precision: 2 decimal places                                           │
│  └─ Range: 0.00 to 999,999,999,999.99                                    │
│                                                                             │
│  👤 status (VARCHAR(10), NULL)                                             │
│  ├─ Choices: 'single', 'married', 'family'                               │
│  ├─ Required for salary tax only                                          │
│  └─ NULL for property and VAT taxes                                       │
│                                                                             │
│  👰 wife_status (VARCHAR(10), DEFAULT='housework')                         │
│  ├─ Choices: 'housework', 'working'                                       │
│  ├─ Only for married status                                               │
│  └─ Affects deductions                                                    │
│                                                                             │
│  👨‍👩‍👧 dependents (INTEGER, DEFAULT=0)                                          │
│  ├─ Number of dependent children                                          │
│  ├─ Range: 0 to 20                                                        │
│  └─ Each dependent: 150,000 KHR/month deduction                           │
│                                                                             │
│  🏠 property_value (DECIMAL(15,2), NULL)                                   │
│  ├─ Value of property in original currency                                │
│  ├─ Only for property tax                                                 │
│  └─ NULL for other tax types                                              │
│                                                                             │
│  🏘️ property_type (VARCHAR(20), NULL)                                      │
│  ├─ Choices: 'house', 'land', 'apartment', 'commercial'                   │
│  ├─ Multipliers: 1.0, 1.2, 0.8, 1.5 respectively                          │
│  └─ NULL for other tax types                                              │
│                                                                             │
│  🧮 tax_amount (DECIMAL(15,2), NOT NULL)                                   │
│  ├─ Calculated tax owed                                                   │
│  ├─ Stored in original currency                                           │
│  └─ Always >= 0                                                           │
│                                                                             │
│  💸 net_income (DECIMAL(15,2), NULL)                                       │
│  ├─ Income after tax (salary) OR                                          │
│  ├─ Total including VAT (VAT) OR                                          │
│  ├─ Property value after tax (property)                                   │
│  └─ Optional field                                                        │
│                                                                             │
│  ⏰ created_at (DATETIME, AUTO_NOW_ADD)                                     │
│  ├─ Timestamp of record creation                                          │
│  ├─ Index: Yes                                                             │
│  └─ Used for sorting and date range queries                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                   │
                        ┌──────────┴──────────┐
                        │                     │
                     1-to-1              Referenced
                   Relationship          by Admin
                        │                     │
┌───────────────────────▼──────────────────────────────────────────────────────┐
│                  📊 TAXCALCULATIONDETAIL TABLE                              │
├────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│  🔑 id (INTEGER, PRIMARY KEY)                                            │
│  └─ Unique identifier                                                    │
│                                                                            │
│  🔗 tax_record_id (INTEGER, FOREIGN KEY, UNIQUE)                         │
│  ├─ References TaxRecord.id                                              │
│  ├─ CASCADE delete: Deletes detail when record deleted                   │
│  └─ One-to-one relationship: Each record has one detail                  │
│                                                                            │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  COMMON FIELDS (All Tax Types)                                           │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                            │
│  % tax_rate (DECIMAL(5,4))                                               │
│  ├─ Applied tax rate (e.g., 0.1000 = 10%)                                │
│  ├─ Range: 0.0000 to 1.0000                                              │
│  └─ Precision: 4 decimal places                                          │
│                                                                            │
│  💾 taxable_amount (DECIMAL(15,2))                                        │
│  ├─ Base amount subject to tax                                           │
│  └─ Stored for audit trail                                               │
│                                                                            │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  SALARY TAX SPECIFIC FIELDS                                              │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                            │
│  👶 deduction_children (DECIMAL(15,2), DEFAULT=0)                        │
│  ├─ 150,000 KHR/month per child                                          │
│  └─ For children under 14 or full-time students                          │
│                                                                            │
│  👰 deduction_wife (DECIMAL(15,2), DEFAULT=0)                            │
│  ├─ 150,000 KHR/month for housewife                                      │
│  └─ 0 KHR if wife is working                                             │
│                                                                            │
│  📋 total_deductions (DECIMAL(15,2), DEFAULT=0)                          │
│  └─ Sum of all family deductions                                         │
│                                                                            │
│  💼 salary_tax_amount (DECIMAL(15,2), DEFAULT=0)                         │
│  ├─ Tax on salary component only                                         │
│  └─ Calculated at progressive rates                                      │
│                                                                            │
│  🎁 grant_benefit_amount (DECIMAL(15,2), DEFAULT=0)                      │
│  ├─ Fringe benefits and grants (Khmer: អត្ថប្រយោជន៍)                      │
│  └─ Taxed separately at 20%                                              │
│                                                                            │
│  📦 grant_tax_amount (DECIMAL(15,2), DEFAULT=0)                          │
│  ├─ 20% tax on grants/benefits                                           │
│  └─ Added to salary tax for total                                        │
│                                                                            │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  PROPERTY TAX SPECIFIC FIELDS                                            │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                            │
│  📐 base_rate (DECIMAL(5,4), DEFAULT=0)                                  │
│  ├─ Standard rate: 0.0010 (0.1% per year)                                │
│  └─ Base before multipliers                                              │
│                                                                            │
│  🏷️ property_type_multiplier (DECIMAL(3,2), DEFAULT=1)                   │
│  ├─ House: 1.0                                                           │
│  ├─ Land: 1.2                                                            │
│  ├─ Apartment: 0.8                                                       │
│  └─ Commercial: 1.5                                                      │
│                                                                            │
│  📈 progressive_multiplier (DECIMAL(3,2), DEFAULT=1)                     │
│  ├─ Value <= 50M: 1.0                                                    │
│  ├─ Value 50M-100M: 1.2                                                  │
│  └─ Value > 100M: 1.5                                                    │
│                                                                            │
│  🎯 final_rate (DECIMAL(5,4), DEFAULT=0)                                 │
│  ├─ final_rate = base × type_multiplier × progressive_multiplier         │
│  └─ Example: 0.001 × 1.2 × 1.5 = 0.0018 (0.18%)                         │
│                                                                            │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│  FLEXIBLE STORAGE                                                        │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                                                            │
│  📦 tax_components (JSON, DEFAULT={})                                     │
│  ├─ Flexible breakdown of tax calculation                                │
│  ├─ Contains detailed component breakdown                                │
│  ├─ Allows easy extension for new tax types                              │
│  └─ Example structure for salary tax:                                    │
│     {                                                                    │
│       "salary_tax": {                                                    │
│         "bracket_1": {"range": "0-1.5M", "rate": "0%", "amount": 0},    │
│         "bracket_5": {"range": "12.5M+", "rate": "20%", "amount": 1M}   │
│       },                                                                 │
│       "grant_tax": {"amount": 0, "rate": "20%"},                         │
│       "deductions": {"children": 300K, "spouse": 150K, "total": 450K}    │
│     }                                                                    │
│                                                                            │
│  ⏰ created_at (DATETIME, AUTO_NOW_ADD)                                   │
│  └─ Timestamp for audit trail                                            │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagram

```
┌──────────────┐
│  User Input  │
│   (Web Form) │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────┐
│  Form Validation             │
│  - Input type check          │
│  - Range validation          │
│  - Required field check      │
└──────┬───────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│  Currency Conversion         │
│  - If USD: Convert to KHR    │
│  - Store in original currency│
└──────┬───────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│  Tax Calculation             │
│  - Apply tax formula         │
│  - Calculate deductions      │
│  - Compute final amount      │
└──────┬───────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│  Create TaxRecord            │
│  - Store input data          │
│  - Store tax_amount          │
│  - Store net_income          │
└──────┬───────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│  Create TaxCalculationDetail │
│  - Store calculation details │
│  - Store tax components      │
│  - Store rates & multipliers │
└──────┬───────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│  Convert Back to Original    │
│  Currency                    │
└──────┬───────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│  Display Results             │
│  - Show tax amount           │
│  - Show net income           │
│  - Show breakdown            │
└──────────────────────────────┘
```

---

## Tax Calculation State Machine

```
START
  │
  ▼
SELECT TAX TYPE
  │
  ├─────────────────┬──────────────────┬─────────────────┐
  │                 │                  │                 │
  ▼                 ▼                  ▼                 ▼
SALARY           PROPERTY             VAT           INVALID
  │                 │                  │
  ├─ Validate    ├─ Validate        ├─ Validate
  │  Income      │  Property Value   │  Sales Amount
  │              │                   │
  ├─ Get Status  ├─ Get Type         ├─ Apply 10%
  │  & Deps      │                   │  Rate
  │              ├─ Get Multipliers  │
  ├─ Calculate  │                   │
  │  Brackets    ├─ Calculate        │
  │              │  Final Rate       │
  ├─ Deduct      │                   │
  │  Family      ├─ Calculate        │
  │              │  Amount           │
  ├─ Calculate  │                   │
  │  Grant Tax   └─────┬─────────────┴──────────────┐
  │                    │                            │
  └────────┬───────────┴────────────────────────────┘
           │
           ▼
    SAVE TO DATABASE
           │
           ├─ TaxRecord
           │   (main data)
           │
           └─ TaxCalculationDetail
               (breakdown)
           │
           ▼
    FORMAT FOR DISPLAY
           │
           ▼
    END

```

---

## Database File Organization

```
tax_calculation/
├── db.sqlite3                      ← SQLite Database (Development)
├── DATABASE_DESIGN.md              ← This Documentation
└── migrations/
    ├── 0001_initial.py             ← Initial Schema
    ├── 0002_alter_options.py       ← Model Updates
    ├── 0003_add_property_fields.py ← Property Tax Support
    ├── 0004_add_currency.py        ← Currency Support
    ├── 0005_add_wife_status.py     ← Spouse Status
    ├── 0006_taxcalculationdetail.py← Detail Records
    ├── 0007_alter_final_rate.py    ← Rate Precision
    └── __init__.py
```

---

## Index Strategy

### Recommended Indexes for High Performance

```python
# In models.py Meta class:
class Meta:
    indexes = [
        models.Index(fields=['tax_type']),                    # Filter by type
        models.Index(fields=['created_at']),                  # Date filtering
        models.Index(fields=['currency']),                    # Currency filtering
        models.Index(fields=['tax_type', 'created_at']),      # Composite index
        models.Index(fields=['created_at', '-tax_amount']),   # Sort by amount
    ]
    unique_together = [
        ('tax_record', 'created_at'),                          # No duplicates
    ]
```

---

## Partition Strategy (for large datasets)

```sql
-- Partition by year
PARTITION BY RANGE (YEAR(created_at)) (
    PARTITION p2022 VALUES LESS THAN (2023),
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p2025 VALUES LESS THAN (2026),
    PARTITION pmax VALUES LESS THAN MAXVALUE
);
```

*This diagram provides a complete visual reference of the database structure.*
