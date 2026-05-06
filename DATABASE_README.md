# Database Documentation Index

## Complete Database Documentation for Tax Calculation System

Welcome to the comprehensive database documentation for the Tax Calculation System. This directory contains all you need to understand, manage, and optimize the database.

---

## 📚 Documentation Files

### 1. **DATABASE_DESIGN.md** - Main Design Document
   - **Purpose**: Complete overview of the database schema
   - **Contents**:
     - Database overview and architecture
     - TaxRecord table schema (13 fields)
     - TaxCalculationDetail table schema (15 fields)
     - Entity Relationship Diagram (ERD)
     - Tax type support matrix
     - JSON schema for tax_components
     - Common SQL queries
     - Performance considerations
     - Validation rules
     - Migration path
     - Backup and recovery procedures
   - **Best For**: Understanding the overall database structure and design decisions
   - **Reading Time**: 15-20 minutes

### 2. **DATABASE_SCHEMA_VISUAL.md** - Visual Reference
   - **Purpose**: Visual representation of database structure
   - **Contents**:
     - Complete ASCII database architecture diagram
     - Detailed field descriptions with icons
     - Data flow diagram
     - Tax calculation state machine
     - Database file organization
     - Index strategy
     - Partition strategy for large datasets
   - **Best For**: Visual learners, quick reference during coding
   - **Reading Time**: 10-15 minutes

### 3. **DATABASE_SQL_REFERENCE.md** - SQL Operations Guide
   - **Purpose**: Practical SQL queries and examples
   - **Contents**:
     - Connection strings for all environments
     - DDL (CREATE TABLE statements)
     - DML (INSERT, UPDATE, DELETE examples)
     - DQL (SELECT and aggregation queries)
     - Window functions for advanced analysis
     - Complex joins
     - Performance optimization queries
     - Backup and recovery commands
     - Transaction examples
     - Maintenance operations
   - **Best For**: Database administrators and developers
   - **Reading Time**: 20-30 minutes

### 4. **DATABASE_ADMIN_GUIDE.md** - Administration & Operations
   - **Purpose**: Day-to-day database management
   - **Contents**:
     - Django ORM operations (Python examples)
     - Automated backup strategies
     - Health checking procedures
     - Disaster recovery plans
     - Performance tuning
     - User management
     - Replication setup
     - Security best practices
     - Troubleshooting guide
     - Migration procedures
   - **Best For**: System administrators and operations teams
   - **Reading Time**: 25-35 minutes

---

## 🗄️ Current Database Schema

### Tables

| Table | Purpose | Records | Size |
|-------|---------|---------|------|
| `calculator_taxrecord` | Main tax calculation records | ~100K | ~50MB |
| `calculator_taxcalculationdetail` | Detailed tax calculation breakdown | ~100K | ~30MB |

### Relationships

```
TaxRecord (1) ──────→ (1) TaxCalculationDetail
   One record         One detail
   has one            per record
   detail
```

### Key Statistics

- **Total Fields**: 28
- **Indexes**: 5+
- **Constraints**: Foreign key (CASCADE)
- **JSON Fields**: 1 (tax_components)
- **Auto Fields**: 1 (id)
- **DateTime Fields**: 2 (created_at)

---

## 📋 Tax Types Supported

### 1. Salary Tax
- **Input**: Income, Family Status, Dependents, Grants
- **Output**: Tax Amount, Net Income, Breakdown by brackets
- **Rates**: Progressive (0%, 5%, 10%, 15%, 20%)
- **Deductions**: Children (150K/month), Spouse (150K/month)

### 2. Property Tax
- **Input**: Property Value, Property Type
- **Output**: Tax Amount, Effective Rate
- **Base Rate**: 0.1% per year
- **Multipliers**: Type (0.8-1.5), Progressive (1.0-1.5)

### 3. VAT Tax
- **Input**: Sales Amount
- **Output**: VAT Amount, Total with VAT
- **Rate**: Fixed 10%
- **Formula**: Sales × 0.10

---

## 🔄 Common Workflows

### Workflow 1: Creating a New Tax Record

```python
# In Django shell or view
from calculator.models import TaxRecord, TaxCalculationDetail

# Step 1: Create main record
record = TaxRecord.objects.create(
    tax_type='salary',
    currency='KHR',
    income=10000000,
    status='married',
    wife_status='housework',
    dependents=1,
    tax_amount=855000,
    net_income=9145000
)

# Step 2: Create calculation details
detail = TaxCalculationDetail.objects.create(
    tax_record=record,
    tax_rate=0.15,
    taxable_amount=9700000,
    deduction_children=150000,
    deduction_wife=150000,
    total_deductions=300000,
    salary_tax_amount=855000,
    grant_tax_amount=0
)
```

### Workflow 2: Querying Records

```python
# Get all salary tax records
records = TaxRecord.objects.filter(tax_type='salary')

# Get records with details
records = TaxRecord.objects.select_related(
    'calculation_details'
).filter(tax_type='salary')

# Get aggregated statistics
from django.db.models import Sum, Avg
stats = TaxRecord.objects.values('tax_type').annotate(
    total=Sum('tax_amount'),
    average=Avg('tax_amount'),
    count=Count('id')
)
```

### Workflow 3: Reporting

```python
# Monthly revenue by tax type
from django.db.models.functions import TruncMonth

monthly = TaxRecord.objects.annotate(
    month=TruncMonth('created_at')
).values('month', 'tax_type').annotate(
    revenue=Sum('tax_amount'),
    records=Count('id')
).order_by('-month')
```

---

## 🚀 Quick Start Guide

### For Developers

1. **Understand the Schema**
   - Read: `DATABASE_DESIGN.md` (Section: Database Schema)
   - Time: 5 minutes

2. **Learn ORM Operations**
   - Read: `DATABASE_ADMIN_GUIDE.md` (Section: Django ORM Operations)
   - Time: 10 minutes

3. **Practice Queries**
   - Run examples in Django shell
   - Time: 15 minutes

### For Database Administrators

1. **Setup and Configuration**
   - Read: `DATABASE_ADMIN_GUIDE.md` (Section: Performance Tuning)
   - Time: 10 minutes

2. **Backup Strategy**
   - Read: `DATABASE_ADMIN_GUIDE.md` (Section: Database Backup Strategy)
   - Time: 5 minutes

3. **Monitoring**
   - Read: `DATABASE_ADMIN_GUIDE.md` (Section: Monitoring and Maintenance)
   - Time: 10 minutes

### For DevOps Engineers

1. **Replication Setup**
   - Read: `DATABASE_ADMIN_GUIDE.md` (Section: Replication Setup)
   - Time: 15 minutes

2. **Security**
   - Read: `DATABASE_ADMIN_GUIDE.md` (Section: Security Best Practices)
   - Time: 10 minutes

3. **Disaster Recovery**
   - Read: `DATABASE_ADMIN_GUIDE.md` (Section: Disaster Recovery Plan)
   - Time: 10 minutes

---

## 🔍 Finding Information

### I need to...

| Task | Document | Section |
|------|----------|---------|
| Understand database structure | DATABASE_DESIGN.md | Database Schema |
| See visual diagrams | DATABASE_SCHEMA_VISUAL.md | Complete Architecture |
| Write SQL queries | DATABASE_SQL_REFERENCE.md | DQL (Data Query Language) |
| Use Django ORM | DATABASE_ADMIN_GUIDE.md | Django ORM Operations |
| Set up backups | DATABASE_ADMIN_GUIDE.md | Database Backup Strategy |
| Troubleshoot issues | DATABASE_ADMIN_GUIDE.md | Troubleshooting Common Issues |
| Optimize performance | DATABASE_DESIGN.md | Database Performance Considerations |
| Migrate databases | DATABASE_ADMIN_GUIDE.md | Migration Guide |
| Understand tax types | DATABASE_DESIGN.md | Tax Type Support Matrix |
| Monitor health | DATABASE_ADMIN_GUIDE.md | Monitoring and Maintenance |

---

## 📊 Data Model Overview

```
┌─────────────────────────────────────────┐
│         TaxRecord (Main)                │
├─────────────────────────────────────────┤
│ • ID (Primary Key)                      │
│ • Tax Type (salary/property/vat)        │
│ • Currency (KHR/USD)                    │
│ • Income/Value/Amount                   │
│ • Status (family structure)             │
│ • Dependents/Property Type              │
│ • Tax Amount (calculated)               │
│ • Net Income (calculated)               │
│ • Created Date/Time (timestamp)         │
└──────────────┬──────────────────────────┘
               │ 1:1
               ▼
┌─────────────────────────────────────────┐
│    TaxCalculationDetail (Details)       │
├─────────────────────────────────────────┤
│ • ID (Primary Key)                      │
│ • Tax Record ID (Foreign Key)           │
│ • Tax Rate (applied)                    │
│ • Taxable Amount                        │
│ • Deductions (if applicable)            │
│ • Tax Components (JSON breakdown)       │
│ • Multipliers (if applicable)           │
│ • Created Date/Time (timestamp)         │
└─────────────────────────────────────────┘
```

---

## 🔒 Security Considerations

### Data Protection
- ✓ Foreign key constraints ensure referential integrity
- ✓ Decimal precision (15,2) prevents rounding errors
- ✓ Auto-timestamps for audit trail
- ✓ Cascade delete maintains consistency

### Access Control
- Use read-only users for reporting
- Implement field-level permissions
- Audit sensitive operations
- Use prepared statements (ORM handles this)

### Backup Security
- Encrypt backups in transit
- Store offline copies
- Test recovery procedures regularly
- Document access procedures

---

## 📈 Scalability Notes

### Current Capacity
- **Records**: 0 - 1,000,000
- **Performance**: Optimal < 100ms queries
- **Storage**: ~100MB per 500K records

### Growth Plan
- **100K records**: No issues expected
- **1M records**: Add indexes on high-frequency filters
- **10M+ records**: Consider table partitioning by year
- **100M+ records**: Archive old records to separate table

### Performance Optimization Priority

1. **Phase 1** (First 100K): Default indexes
2. **Phase 2** (100K-1M): Add composite indexes
3. **Phase 3** (1M+): Implement partitioning
4. **Phase 4** (10M+): Archive old records

---

## 🔧 Common Commands

### Django Management Commands

```bash
# Check database
python manage.py check

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Dump data
python manage.py dumpdata > data.json

# Load data
python manage.py loaddata data.json

# Shell access
python manage.py shell
```

### MySQL Commands

```bash
# Backup
mysqldump -u user -p database > backup.sql

# Restore
mysql -u user -p database < backup.sql

# Check status
mysql -e "SHOW DATABASE STATUS;"
```

---

## 📞 Support & Documentation

### For Questions About

| Topic | Documentation |
|-------|---|
| Schema Design | DATABASE_DESIGN.md |
| Visual Diagrams | DATABASE_SCHEMA_VISUAL.md |
| SQL Syntax | DATABASE_SQL_REFERENCE.md |
| Operations | DATABASE_ADMIN_GUIDE.md |

### Version Information

- **Database Version**: 1.0 (Current)
- **Documentation Updated**: May 6, 2026
- **Django Version**: 3.2+
- **Python Version**: 3.8+

---

## 🎯 Next Steps

### Immediate Actions
1. ✓ Review DATABASE_DESIGN.md
2. ✓ Set up automated backups
3. ✓ Test disaster recovery
4. ✓ Configure monitoring

### Ongoing Maintenance
- Review performance monthly
- Archive old records yearly
- Test backups quarterly
- Update documentation as needed

---

## 📚 Additional Resources

### Related Files
- `calculator/models.py` - Django model definitions
- `calculator/views.py` - View functions
- `calculator/forms.py` - Form definitions
- `migrations/` - Database migration files

### External Documentation
- [Django ORM Documentation](https://docs.djangoproject.com/en/stable/topics/db/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

*Documentation Package: Tax Calculation System Database*  
*Last Updated: May 6, 2026*  
*Version: 1.0*
