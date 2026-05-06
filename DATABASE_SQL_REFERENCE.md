# Database SQL Reference Guide

## Connection Strings

### Development (SQLite)
```
sqlite:///db.sqlite3
```

### Production (PostgreSQL)
```
postgresql://user:password@localhost:5432/tax_calculation
```

### Production (MySQL)
```
mysql://user:password@localhost:3306/tax_calculation
```

---

## DDL (Data Definition Language)

### Create Tables

```sql
-- TaxRecord Table
CREATE TABLE calculator_taxrecord (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    tax_type VARCHAR(10) NOT NULL,
    currency VARCHAR(3) DEFAULT 'KHR',
    income DECIMAL(15, 2) NOT NULL,
    status VARCHAR(10) NULL,
    wife_status VARCHAR(10) DEFAULT 'housework',
    dependents INTEGER DEFAULT 0,
    property_value DECIMAL(15, 2) NULL,
    property_type VARCHAR(20) NULL,
    tax_amount DECIMAL(15, 2) NOT NULL,
    net_income DECIMAL(15, 2) NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_tax_type (tax_type),
    INDEX idx_created_at (created_at),
    INDEX idx_currency (currency),
    INDEX idx_tax_type_created (tax_type, created_at)
);

-- TaxCalculationDetail Table
CREATE TABLE calculator_taxcalculationdetail (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    tax_record_id INTEGER NOT NULL UNIQUE,
    tax_rate DECIMAL(5, 4) NOT NULL,
    taxable_amount DECIMAL(15, 2) NOT NULL,
    deduction_children DECIMAL(15, 2) DEFAULT 0,
    deduction_wife DECIMAL(15, 2) DEFAULT 0,
    total_deductions DECIMAL(15, 2) DEFAULT 0,
    salary_tax_amount DECIMAL(15, 2) DEFAULT 0,
    grant_benefit_amount DECIMAL(15, 2) DEFAULT 0,
    grant_tax_amount DECIMAL(15, 2) DEFAULT 0,
    base_rate DECIMAL(5, 4) DEFAULT 0,
    property_type_multiplier DECIMAL(3, 2) DEFAULT 1,
    progressive_multiplier DECIMAL(3, 2) DEFAULT 1,
    final_rate DECIMAL(5, 4) DEFAULT 0,
    tax_components JSON DEFAULT '{}',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (tax_record_id) REFERENCES calculator_taxrecord(id) 
        ON DELETE CASCADE,
    INDEX idx_tax_record_id (tax_record_id),
    INDEX idx_created_at (created_at)
);
```

---

## DML (Data Manipulation Language)

### INSERT Operations

```sql
-- Insert a single salary tax record
INSERT INTO calculator_taxrecord 
(tax_type, currency, income, status, wife_status, dependents, tax_amount, net_income)
VALUES 
('salary', 'KHR', 10000000, 'married', 'housework', 1, 855000, 9145000);

-- Insert a property tax record
INSERT INTO calculator_taxrecord
(tax_type, currency, income, property_value, property_type, tax_amount, net_income)
VALUES
('property', 'KHR', 50000000, 50000000, 'house', 50000, 49950000);

-- Insert a VAT tax record
INSERT INTO calculator_taxrecord
(tax_type, currency, income, tax_amount, net_income)
VALUES
('vat', 'USD', 1000, 100, 1100);

-- Insert calculation details for salary tax
INSERT INTO calculator_taxcalculationdetail
(tax_record_id, tax_rate, taxable_amount, deduction_children, deduction_wife, 
 total_deductions, salary_tax_amount, grant_tax_amount, tax_components)
VALUES
(1, 0.15, 9700000, 150000, 150000, 300000, 855000, 0, 
 '{"salary_tax": {"bracket": 4, "rate": 0.15}, "deductions": {"children": 150000, "spouse": 150000}}');
```

### SELECT Operations

```sql
-- Get all salary tax records
SELECT * FROM calculator_taxrecord 
WHERE tax_type = 'salary'
ORDER BY created_at DESC;

-- Get all records created today
SELECT * FROM calculator_taxrecord
WHERE DATE(created_at) = CURDATE()
ORDER BY created_at DESC;

-- Get records within a date range
SELECT * FROM calculator_taxrecord
WHERE created_at BETWEEN '2024-01-01' AND '2024-12-31'
ORDER BY created_at DESC;

-- Get records by currency
SELECT * FROM calculator_taxrecord
WHERE currency = 'KHR'
ORDER BY created_at DESC;

-- Get all records with their details (LEFT JOIN)
SELECT 
    tr.id,
    tr.tax_type,
    tr.currency,
    tr.income,
    tr.tax_amount,
    tr.net_income,
    tcd.tax_rate,
    tcd.total_deductions,
    tcd.salary_tax_amount,
    tr.created_at
FROM calculator_taxrecord tr
LEFT JOIN calculator_taxcalculationdetail tcd
    ON tr.id = tcd.tax_record_id
ORDER BY tr.created_at DESC;

-- Get calculation details for a specific record
SELECT * FROM calculator_taxcalculationdetail
WHERE tax_record_id = 1;

-- Get JSON field (PostgreSQL)
SELECT 
    id,
    tax_components->>'salary_tax' as salary_breakdown,
    tax_components->>'deductions' as deductions
FROM calculator_taxcalculationdetail
WHERE tax_record_id = 1;
```

### UPDATE Operations

```sql
-- Update tax amount for a record
UPDATE calculator_taxrecord
SET tax_amount = 900000
WHERE id = 1;

-- Update multiple records
UPDATE calculator_taxrecord
SET currency = 'USD'
WHERE tax_type = 'vat'
  AND created_at >= '2024-01-01';

-- Update with calculation
UPDATE calculator_taxrecord
SET net_income = income - tax_amount
WHERE tax_type IN ('salary', 'property');

-- Update JSON field (PostgreSQL)
UPDATE calculator_taxcalculationdetail
SET tax_components = jsonb_set(
    tax_components,
    '{salary_tax, rate}',
    '0.20'::jsonb
)
WHERE id = 1;
```

### DELETE Operations

```sql
-- Delete a single record (cascades to details)
DELETE FROM calculator_taxrecord
WHERE id = 1;

-- Delete records older than 2 years
DELETE FROM calculator_taxrecord
WHERE created_at < DATE_SUB(NOW(), INTERVAL 2 YEAR);

-- Delete by type
DELETE FROM calculator_taxrecord
WHERE tax_type = 'salary'
  AND created_at < '2023-01-01';
```

---

## DQL (Data Query Language)

### Aggregation Queries

```sql
-- Total tax collected by type
SELECT 
    tax_type,
    COUNT(*) as record_count,
    SUM(tax_amount) as total_tax,
    AVG(tax_amount) as avg_tax,
    MIN(tax_amount) as min_tax,
    MAX(tax_amount) as max_tax
FROM calculator_taxrecord
GROUP BY tax_type
ORDER BY total_tax DESC;

-- Tax collected by currency
SELECT 
    currency,
    SUM(tax_amount) as total_tax,
    AVG(income) as avg_income,
    COUNT(*) as count
FROM calculator_taxrecord
GROUP BY currency;

-- Tax collected by date
SELECT 
    DATE(created_at) as tax_date,
    COUNT(*) as count,
    SUM(tax_amount) as daily_total,
    AVG(tax_amount) as daily_avg
FROM calculator_taxrecord
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY DATE(created_at)
ORDER BY tax_date DESC;

-- Monthly revenue report
SELECT 
    DATE_TRUNC('month', created_at) as month,
    tax_type,
    COUNT(*) as records,
    SUM(tax_amount) as revenue
FROM calculator_taxrecord
GROUP BY DATE_TRUNC('month', created_at), tax_type
ORDER BY month DESC, revenue DESC;

-- Average tax by status (salary tax)
SELECT 
    status,
    COUNT(*) as count,
    AVG(income) as avg_income,
    AVG(tax_amount) as avg_tax,
    ROUND(AVG(tax_amount) / AVG(income) * 100, 2) as effective_rate
FROM calculator_taxrecord
WHERE tax_type = 'salary'
GROUP BY status
ORDER BY avg_tax DESC;

-- Property tax analysis
SELECT 
    property_type,
    COUNT(*) as count,
    AVG(income) as avg_property_value,
    AVG(tax_amount) as avg_tax,
    SUM(tax_amount) as total_tax
FROM calculator_taxrecord
WHERE tax_type = 'property'
GROUP BY property_type
ORDER BY total_tax DESC;

-- High earners (salary > 50M/month)
SELECT 
    id,
    income,
    tax_amount,
    status,
    dependents,
    ROUND((tax_amount / income) * 100, 2) as tax_rate_percent
FROM calculator_taxrecord
WHERE tax_type = 'salary'
  AND income > 50000000
ORDER BY income DESC;
```

### Window Functions (PostgreSQL/MySQL 8+)

```sql
-- Running total of tax collected
SELECT 
    created_at,
    tax_amount,
    SUM(tax_amount) OVER (ORDER BY created_at) as running_total,
    AVG(tax_amount) OVER (
        ORDER BY created_at 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) as moving_avg_7day
FROM calculator_taxrecord
WHERE tax_type = 'salary'
ORDER BY created_at DESC;

-- Rank records by tax amount
SELECT 
    id,
    tax_type,
    income,
    tax_amount,
    RANK() OVER (PARTITION BY tax_type ORDER BY tax_amount DESC) as rank_by_type
FROM calculator_taxrecord
ORDER BY tax_type, rank_by_type;

-- Percentile analysis
SELECT 
    id,
    tax_amount,
    PERCENT_RANK() OVER (ORDER BY tax_amount) * 100 as percentile
FROM calculator_taxrecord
WHERE tax_type = 'salary'
ORDER BY tax_amount DESC;
```

### Complex Joins

```sql
-- Full record with all details and calculations
SELECT 
    tr.id,
    tr.tax_type,
    tr.currency,
    tr.income,
    tr.status,
    tr.dependents,
    tr.tax_amount,
    tr.net_income,
    tcd.tax_rate,
    tcd.total_deductions,
    tcd.salary_tax_amount,
    tcd.grant_tax_amount,
    CASE 
        WHEN tcd.salary_tax_amount > 0 
        THEN ROUND((tcd.salary_tax_amount / tr.income) * 100, 2)
        ELSE 0
    END as effective_tax_rate,
    tr.created_at
FROM calculator_taxrecord tr
LEFT JOIN calculator_taxcalculationdetail tcd
    ON tr.id = tcd.tax_record_id
WHERE tr.created_at >= DATE_SUB(NOW(), INTERVAL 90 DAY)
ORDER BY tr.created_at DESC;

-- Compare records side by side
SELECT 
    tr1.id as record_1_id,
    tr2.id as record_2_id,
    tr1.tax_type,
    tr1.income as income_1,
    tr2.income as income_2,
    tr1.tax_amount as tax_1,
    tr2.tax_amount as tax_2,
    (tr2.tax_amount - tr1.tax_amount) as difference
FROM calculator_taxrecord tr1
JOIN calculator_taxrecord tr2
    ON tr1.tax_type = tr2.tax_type
WHERE tr1.created_at > tr2.created_at
  AND DATE(tr1.created_at) = DATE(tr2.created_at)
LIMIT 10;
```

---

## Performance Optimization Queries

### Check Index Usage

```sql
-- MySQL: Show index statistics
SHOW STATISTICS FROM calculator_taxrecord WHERE Seq_in_index = 1;

-- PostgreSQL: Check index size
SELECT 
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) as index_size
FROM pg_indexes
JOIN pg_class ON indexrelname = pg_indexes.indexname
WHERE tablename = 'calculator_taxrecord'
ORDER BY pg_relation_size(indexrelid) DESC;
```

### Query Execution Plans

```sql
-- MySQL: EXPLAIN ANALYZE
EXPLAIN ANALYZE
SELECT * FROM calculator_taxrecord
WHERE tax_type = 'salary' AND created_at > '2024-01-01';

-- PostgreSQL: EXPLAIN ANALYZE with BUFFERS
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM calculator_taxrecord
WHERE tax_type = 'salary' AND created_at > '2024-01-01';
```

### Query Optimization Tips

```sql
-- ✓ GOOD: Uses index on tax_type and created_at
SELECT * FROM calculator_taxrecord
WHERE tax_type = 'salary' 
  AND created_at > '2024-01-01'
ORDER BY created_at DESC;

-- ✗ BAD: Function on indexed column (won't use index)
SELECT * FROM calculator_taxrecord
WHERE UPPER(tax_type) = 'SALARY';
-- Solution: Compare directly
SELECT * FROM calculator_taxrecord
WHERE tax_type = 'salary';

-- ✗ BAD: OR conditions may not use index efficiently
SELECT * FROM calculator_taxrecord
WHERE tax_type = 'salary' OR tax_type = 'property';
-- Solution: Use IN clause
SELECT * FROM calculator_taxrecord
WHERE tax_type IN ('salary', 'property');

-- ✓ GOOD: Limit results for large datasets
SELECT * FROM calculator_taxrecord
WHERE created_at > DATE_SUB(NOW(), INTERVAL 30 DAY)
LIMIT 100;
```

---

## Backup and Recovery

### MySQL Backup

```sql
-- Full database backup
mysqldump -u user -p tax_calculation > backup_20240506.sql

-- Specific table backup
mysqldump -u user -p tax_calculation calculator_taxrecord > taxrecord_backup.sql

-- Restore from backup
mysql -u user -p tax_calculation < backup_20240506.sql
```

### PostgreSQL Backup

```sql
-- Full database backup
pg_dump tax_calculation > backup_20240506.sql

-- Custom format (compressed)
pg_dump -F c tax_calculation > backup_20240506.dump

-- Restore from backup
psql tax_calculation < backup_20240506.sql

-- Restore from custom format
pg_restore -d tax_calculation backup_20240506.dump
```

---

## Transaction Examples

```sql
-- Transaction for creating record and details
START TRANSACTION;

INSERT INTO calculator_taxrecord 
(tax_type, currency, income, status, tax_amount)
VALUES ('salary', 'KHR', 10000000, 'married', 855000);

SET @last_id = LAST_INSERT_ID();

INSERT INTO calculator_taxcalculationdetail
(tax_record_id, tax_rate, taxable_amount, salary_tax_amount)
VALUES (@last_id, 0.15, 9700000, 855000);

COMMIT;

-- Rollback on error
START TRANSACTION;
-- ... operations ...
ROLLBACK; -- Undo all changes
```

---

## Maintenance Operations

```sql
-- Optimize table (MySQL)
OPTIMIZE TABLE calculator_taxrecord;
OPTIMIZE TABLE calculator_taxcalculationdetail;

-- Analyze table (MySQL)
ANALYZE TABLE calculator_taxrecord;

-- VACUUM (PostgreSQL)
VACUUM ANALYZE calculator_taxrecord;

-- Check table integrity
CHECK TABLE calculator_taxrecord;

-- Repair table if corrupted
REPAIR TABLE calculator_taxrecord;
```

---

## Export/Import Data

### CSV Export

```sql
-- MySQL: Export to CSV
SELECT * INTO OUTFILE '/tmp/taxrecords.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
FROM calculator_taxrecord;

-- PostgreSQL: Copy to CSV
COPY calculator_taxrecord TO '/tmp/taxrecords.csv' WITH CSV;
```

### CSV Import

```sql
-- MySQL: Import from CSV
LOAD DATA LOCAL INFILE '/tmp/taxrecords.csv'
INTO TABLE calculator_taxrecord
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';

-- PostgreSQL: Copy from CSV
COPY calculator_taxrecord FROM '/tmp/taxrecords.csv' WITH CSV;
```

---

## Common Administrator Tasks

```sql
-- Get database size
-- MySQL
SELECT 
    table_schema,
    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS 'Size in MB'
FROM information_schema.tables
WHERE table_schema = 'tax_calculation'
GROUP BY table_schema;

-- PostgreSQL
SELECT 
    pg_database.datname,
    pg_size_pretty(pg_database_size(pg_database.datname)) AS size
FROM pg_database
WHERE datname = 'tax_calculation';

-- Get record count by type
SELECT 
    tax_type,
    COUNT(*) as count
FROM calculator_taxrecord
GROUP BY tax_type;

-- Remove duplicate records
DELETE FROM calculator_taxrecord
WHERE id NOT IN (
    SELECT MAX(id)
    FROM calculator_taxrecord
    GROUP BY tax_type, income, currency
);

-- Archive old records (to archive table)
INSERT INTO calculator_taxrecord_archive
SELECT * FROM calculator_taxrecord
WHERE created_at < DATE_SUB(NOW(), INTERVAL 2 YEAR);

DELETE FROM calculator_taxrecord
WHERE created_at < DATE_SUB(NOW(), INTERVAL 2 YEAR);
```

*Reference guide for SQL operations on Tax Calculation database*
