# Database Administration Guide

## Quick Reference Card

### Database Connection

| Environment | Host | Port | Database | User |
|-------------|------|------|----------|------|
| Development | SQLite (file) | N/A | db.sqlite3 | N/A |
| Production | localhost | 3306 | tax_calculation | tax_user |
| Staging | staging-db | 3306 | tax_calc_staging | tax_stage |

---

## Django ORM Operations (Instead of Raw SQL)

### Using Django Shell

```python
# Access Django shell
python manage.py shell

# ================== IMPORTS ==================
from calculator.models import TaxRecord, TaxCalculationDetail
from django.db.models import Sum, Avg, Count, Q
from datetime import datetime, timedelta

# ================== CREATE (INSERT) ==================
# Create a salary tax record
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

# Create calculation detail
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

# ================== READ (SELECT) ==================
# Get all salary tax records
salary_records = TaxRecord.objects.filter(tax_type='salary')

# Get records from specific date
today_records = TaxRecord.objects.filter(
    created_at__date=datetime.today()
)

# Get records within date range
from datetime import date
start_date = date(2024, 1, 1)
end_date = date(2024, 12, 31)
yearly_records = TaxRecord.objects.filter(
    created_at__date__gte=start_date,
    created_at__date__lte=end_date
)

# Get single record by ID
record = TaxRecord.objects.get(id=1)

# Get record with related details
record = TaxRecord.objects.select_related('calculation_details').get(id=1)

# Get all records ordered by date
records = TaxRecord.objects.order_by('-created_at')

# Get first and last records
first_record = TaxRecord.objects.order_by('created_at').first()
last_record = TaxRecord.objects.order_by('-created_at').first()

# Count records by type
salary_count = TaxRecord.objects.filter(tax_type='salary').count()

# ================== UPDATE ==================
# Update single record
record = TaxRecord.objects.get(id=1)
record.tax_amount = 900000
record.save()

# Update multiple records at once
TaxRecord.objects.filter(
    tax_type='salary',
    created_at__year=2024
).update(currency='KHR')

# Conditional update
TaxRecord.objects.filter(
    tax_type='salary',
    income__gte=50000000
).update(status='family')

# ================== DELETE ==================
# Delete single record (cascades to details)
record = TaxRecord.objects.get(id=1)
record.delete()

# Delete multiple records
TaxRecord.objects.filter(
    created_at__lt=datetime.now() - timedelta(days=730)
).delete()

# Delete by type
TaxRecord.objects.filter(tax_type='property').delete()

# ================== AGGREGATION ==================
# Sum of all taxes collected
total_tax = TaxRecord.objects.aggregate(Sum('tax_amount'))
# Returns: {'tax_amount__sum': 5000000}

# Count records by type
from django.db.models import Count, Sum
stats = TaxRecord.objects.values('tax_type').annotate(
    count=Count('id'),
    total=Sum('tax_amount'),
    avg=Avg('tax_amount')
).order_by('-total')

# Monthly revenue
from django.db.models.functions import TruncDate, TruncMonth
monthly = TaxRecord.objects.annotate(
    month=TruncMonth('created_at')
).values('month').annotate(
    revenue=Sum('tax_amount'),
    count=Count('id')
).order_by('-month')

# Average tax by status
avg_by_status = TaxRecord.objects.filter(
    tax_type='salary'
).values('status').annotate(
    avg_tax=Avg('tax_amount'),
    count=Count('id')
).order_by('-avg_tax')

# ================== FILTERING ==================
# Complex filters with Q objects
from django.db.models import Q

# OR condition: salary OR property tax
mixed = TaxRecord.objects.filter(
    Q(tax_type='salary') | Q(tax_type='property')
)

# AND condition with OR: (salary AND KHR) OR (VAT AND USD)
complex_filter = TaxRecord.objects.filter(
    Q(tax_type='salary', currency='KHR') |
    Q(tax_type='vat', currency='USD')
)

# NOT condition: Not salary tax
not_salary = TaxRecord.objects.exclude(tax_type='salary')

# Multiple conditions
high_earners = TaxRecord.objects.filter(
    tax_type='salary',
    income__gte=50000000,
    status='family'
)

# ================== PAGINATION ==================
from django.core.paginator import Paginator

# Get all salary records, page 1, 10 per page
paginator = Paginator(
    TaxRecord.objects.filter(tax_type='salary'),
    10
)
page1 = paginator.get_page(1)
records = page1.object_list
has_next = page1.has_next()
has_prev = page1.has_previous()

# ================== PERFORMANCE ==================
# Use select_related for foreign key
records = TaxRecord.objects.select_related(
    'calculation_details'
).filter(tax_type='salary')

# Use prefetch_related for reverse foreign key
from django.db.models import Prefetch
records = TaxRecord.objects.prefetch_related(
    'calculation_details'
)

# Only get specific fields (more efficient)
records = TaxRecord.objects.values_list(
    'id', 'tax_type', 'income', 'tax_amount'
).filter(tax_type='salary')

# Use distinct to remove duplicates
unique_types = TaxRecord.objects.values_list(
    'tax_type', flat=True
).distinct()

# ================== BULK OPERATIONS ==================
# Bulk create records
records_to_create = [
    TaxRecord(tax_type='salary', income=10000000, tax_amount=1000000),
    TaxRecord(tax_type='property', income=50000000, tax_amount=50000),
    TaxRecord(tax_type='vat', income=1000, tax_amount=100),
]
TaxRecord.objects.bulk_create(records_to_create)

# Bulk update
from django.db.models import F
TaxRecord.objects.filter(
    tax_type='salary'
).update(net_income=F('income') - F('tax_amount'))

# ================== USEFUL QUERIES ==================
# Get latest record for each tax type
from django.db.models import Max
latest = TaxRecord.objects.values('tax_type').annotate(
    max_id=Max('id')
).values_list('max_id', flat=True)
latest_records = TaxRecord.objects.filter(id__in=latest)

# Get top 5 highest tax amounts
top_5 = TaxRecord.objects.order_by('-tax_amount')[:5]

# Get all records modified in last 7 days
week_ago = datetime.now() - timedelta(days=7)
recent = TaxRecord.objects.filter(created_at__gte=week_ago)

# Check if record exists
exists = TaxRecord.objects.filter(id=1).exists()

# Count total records
total = TaxRecord.objects.count()

# Get or create pattern
record, created = TaxRecord.objects.get_or_create(
    id=1,
    defaults={
        'tax_type': 'salary',
        'income': 10000000,
        'tax_amount': 1000000
    }
)

# Update or create pattern
record, created = TaxRecord.objects.update_or_create(
    id=1,
    defaults={
        'tax_type': 'salary',
        'income': 12000000,
        'tax_amount': 1200000
    }
)
```

---

## Database Backup Strategy

### Automated Daily Backups

```bash
#!/bin/bash
# backup_database.sh

BACKUP_DIR="/var/backups/tax_calculation"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="tax_calculation"

# Create backup directory if not exists
mkdir -p $BACKUP_DIR

# Backup with compression
mysqldump -u tax_user -p"$DB_PASSWORD" $DB_NAME | \
    gzip > "$BACKUP_DIR/backup_$DATE.sql.gz"

# Keep only last 30 days of backups
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +30 -delete

# Log backup status
echo "$(date): Backup completed - backup_$DATE.sql.gz" >> $BACKUP_DIR/backup.log
```

### Schedule with Cron

```bash
# Add to crontab (runs daily at 2 AM)
0 2 * * * /path/to/backup_database.sh

# Run cron
crontab -e
```

---

## Monitoring and Maintenance

### Check Database Health

```python
# health_check.py
from django.core.management.base import BaseCommand
from django.db import connection
from calculator.models import TaxRecord, TaxCalculationDetail

class Command(BaseCommand):
    help = 'Check database health'

    def handle(self, *args, **options):
        try:
            # Test database connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            
            # Count records
            total_records = TaxRecord.objects.count()
            detail_records = TaxCalculationDetail.objects.count()
            
            # Check for orphaned records
            orphaned = TaxRecord.objects.filter(
                calculation_details__isnull=True
            ).count()
            
            print(f"✓ Database Connected")
            print(f"✓ Total Records: {total_records}")
            print(f"✓ Detail Records: {detail_records}")
            print(f"⚠ Orphaned Records: {orphaned}")
            
            if orphaned > 0:
                self.stdout.write(
                    self.style.WARNING(
                        f"Found {orphaned} records without details"
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS("Database is healthy!")
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Database Error: {str(e)}")
            )
```

### Run Health Check

```bash
python manage.py health_check_db
```

---

## Disaster Recovery Plan

### Steps for Recovery

1. **Stop the application**
   ```bash
   systemctl stop gunicorn
   systemctl stop nginx
   ```

2. **Check backup integrity**
   ```bash
   gunzip -t backup_20240506.sql.gz
   ```

3. **Restore from backup**
   ```bash
   gunzip < backup_20240506.sql.gz | mysql -u tax_user -p tax_calculation
   ```

4. **Verify restoration**
   ```python
   python manage.py shell
   from calculator.models import TaxRecord
   TaxRecord.objects.count()  # Should show expected count
   ```

5. **Restart application**
   ```bash
   systemctl start gunicorn
   systemctl start nginx
   ```

---

## Performance Tuning

### Database Configuration

#### MySQL Configuration (my.cnf)

```ini
[mysqld]
# Buffer pool size (50-80% of RAM for dedicated DB server)
innodb_buffer_pool_size = 4G

# Log file size (Larger = better performance, slower recovery)
innodb_log_file_size = 512M

# Thread pool
innodb_thread_concurrency = 0

# Query cache
query_cache_size = 256M
query_cache_type = 1

# Connection pool
max_connections = 100

# Slow query log
slow_query_log = 1
slow_query_log_file = /var/log/mysql/slow.log
long_query_time = 2
```

#### PostgreSQL Configuration (postgresql.conf)

```ini
# Memory settings
shared_buffers = 4GB
effective_cache_size = 12GB
maintenance_work_mem = 1GB
work_mem = 10MB

# Connection settings
max_connections = 100
max_prepared_transactions = 100

# WAL settings
wal_buffers = 16MB
checkpoint_timeout = 15min

# Enable query analysis
log_statement = 'all'
log_duration = on
log_min_duration_statement = 1000  # Log queries > 1 second
```

---

## User Management

### Create Database User

```sql
-- MySQL
CREATE USER 'tax_user'@'localhost' IDENTIFIED BY 'secure_password_123';
GRANT ALL PRIVILEGES ON tax_calculation.* TO 'tax_user'@'localhost';
FLUSH PRIVILEGES;

-- PostgreSQL
CREATE USER tax_user WITH PASSWORD 'secure_password_123';
GRANT ALL PRIVILEGES ON DATABASE tax_calculation TO tax_user;
```

### Setup Read-Only User

```sql
-- MySQL
CREATE USER 'tax_reader'@'localhost' IDENTIFIED BY 'readonly_pass';
GRANT SELECT ON tax_calculation.* TO 'tax_reader'@'localhost';
FLUSH PRIVILEGES;

-- PostgreSQL
CREATE USER tax_reader WITH PASSWORD 'readonly_pass';
GRANT CONNECT ON DATABASE tax_calculation TO tax_reader;
GRANT USAGE ON SCHEMA public TO tax_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO tax_reader;
```

---

## Replication Setup (High Availability)

### Master-Slave Replication (MySQL)

**On Master Server:**
```sql
-- Enable binary logging (in my.cnf)
-- [mysqld]
-- log_bin = mysql-bin
-- server-id = 1

-- Create replication user
CREATE USER 'repl'@'slave_ip' IDENTIFIED BY 'repl_password';
GRANT REPLICATION SLAVE ON *.* TO 'repl'@'slave_ip';

-- Get master status
SHOW MASTER STATUS;
-- Note: File and Position for slave
```

**On Slave Server:**
```sql
-- Configure slave
CHANGE MASTER TO
  MASTER_HOST='master_ip',
  MASTER_USER='repl',
  MASTER_PASSWORD='repl_password',
  MASTER_LOG_FILE='mysql-bin.000001',
  MASTER_LOG_POS=154;

-- Start replication
START SLAVE;

-- Check slave status
SHOW SLAVE STATUS\G
```

---

## Security Best Practices

### 1. Connection Security
- Always use SSL for remote connections
- Use SSH tunneling for management connections
- Change default passwords immediately

### 2. Firewall Rules
```bash
# Allow only application server to access database
iptables -A INPUT -p tcp --dport 3306 -s APP_SERVER_IP -j ACCEPT
iptables -A INPUT -p tcp --dport 3306 -j DROP
```

### 3. Data Encryption
```python
# In settings.py for production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'ssl': {
                'ca': '/path/to/ca.pem',
                'cert': '/path/to/client-cert.pem',
                'key': '/path/to/client-key.pem',
            }
        }
    }
}
```

### 4. Regular Updates
```bash
# Update MySQL
apt-get update
apt-get upgrade mysql-server

# Check for vulnerabilities
apt-get upgrade
security-check database
```

---

## Troubleshooting Common Issues

### Issue: Slow Queries

```sql
-- Find slow queries
SELECT * FROM mysql.slow_log;

-- Enable profiling for specific query
SET PROFILING=1;
SELECT * FROM calculator_taxrecord WHERE tax_type='salary';
SHOW PROFILE ALL;

-- Get query execution plan
EXPLAIN SELECT * FROM calculator_taxrecord WHERE tax_type='salary'\G
```

### Issue: Disk Space

```bash
# Check disk usage
du -sh /var/lib/mysql

# Check largest tables
mysql -e "SELECT table_name, ROUND(((data_length + index_length) / 1024 / 1024), 2) AS size_mb FROM information_schema.TABLES WHERE table_schema = 'tax_calculation' ORDER BY size_mb DESC;"

# Archive old data
python manage.py archive_old_records --days=730
```

### Issue: Connection Errors

```bash
# Check if MySQL service is running
systemctl status mysql

# Restart service
systemctl restart mysql

# Check error log
tail -n 50 /var/log/mysql/error.log

# Test connection
mysql -u tax_user -p tax_calculation -e "SELECT 1;"
```

---

## Migration Guide

### From SQLite to MySQL

```bash
# 1. Export data from SQLite
python manage.py dumpdata > data.json

# 2. Update settings.py
# Change database to MySQL

# 3. Run migrations on new database
python manage.py migrate

# 4. Load data
python manage.py loaddata data.json

# 5. Verify data integrity
python manage.py health_check_db
```

---

*Database Administration Guide - Last Updated: May 6, 2026*
