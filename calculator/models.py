from django.db import models


class TaxRecord(models.Model):
    TAX_TYPE_CHOICES = [
        ('salary', 'ពន្ធលើប្រាក់បៀវតន៏'),
        ('property', 'ពន្ធអាក'),
        ('vat', 'ពន្ធតម្លៃបន្ថែម'),
    ]
    
    CURRENCY_CHOICES = [
        ('KHR', '៛ រៀលកម្ពុជា'),
        ('USD', '$ ដុល្លារអាមេរិក'),
    ]
    
    STATUS_CHOICES = [
        ('single', 'នៅលីវ'),
        ('married', 'រៀបការ'),
        ('family', 'មានកូន'),
    ]
    
    WIFE_STATUS_CHOICES = [
        ('housework', 'ធ្វើការផ្ទះ'),
        ('working', 'ធ្វើការ'),
    ]

    tax_type = models.CharField(max_length=10, choices=TAX_TYPE_CHOICES, default='salary', verbose_name="ប្រភេទពន្ធ")
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='KHR', verbose_name="រូបិយប័ណ្ណ")
    income = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="ចំណូល/តម្លៃអចលនទ្រព្យ")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name="ស្ថានភាពគ្រួសារ", blank=True, null=True)
    wife_status = models.CharField(max_length=10, choices=WIFE_STATUS_CHOICES, default='housework', verbose_name="ស្ថានភាពប្រពន្ធ", blank=True, null=True)
    dependents = models.IntegerField(default=0, verbose_name="អ្នកអាស្រ័យ (នាក់)", blank=True, null=True)
    property_value = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="តម្លៃអចលនទ្រព្យ", blank=True, null=True)
    property_type = models.CharField(max_length=20, verbose_name="ប្រភេទអចលនទ្រព្យ", blank=True, null=True)
    tax_amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="ពន្ធប៉ាន់ស្មាន")
    net_income = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="ប្រាក់សុទ្ធ/តម្លៃសុទ្ធ", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="កាលបរិច្ឆេទ")

    class Meta:
        verbose_name = "កំណត់ត្រាពន្ធ"
        verbose_name_plural = "កំណត់ត្រាពន្ធ"
        ordering = ['-created_at']

    def __str__(self):
        if self.tax_type == 'salary':
            return f"ពន្ធប្រាក់បៀវតន៏: {self.income:,}៛ → ពន្ធ: {self.tax_amount:,}៛ (ថ្ងៃ {self.created_at.date()})"
        elif self.tax_type == 'property':
            return f"ពន្ធអាក: {self.property_value:,}៛ → ពន្ធ: {self.tax_amount:,}៛ (ថ្ងៃ {self.created_at.date()})"
        elif self.tax_type == 'vat':
            return f"ពន្ធតម្លៃបន្ថែម: {self.income:,}៛ → ពន្ធ: {self.tax_amount:,}៛ (ថ្ងៃ {self.created_at.date()})"
        else:
            return f"ពន្ធ: {self.income:,}៛ → ពន្ធ: {self.tax_amount:,}៛ (ថ្ងៃ {self.created_at.date()})"


class TaxCalculationDetail(models.Model):
    """
    Stores detailed breakdown of tax calculations for each TaxRecord.
    Contains the components that make up the final tax amount.
    """
    tax_record = models.OneToOneField(TaxRecord, on_delete=models.CASCADE, related_name='calculation_details', verbose_name="កំណត់ត្រាពន្ធ")

    # Common fields for all tax types
    tax_rate = models.DecimalField(max_digits=5, decimal_places=4, verbose_name="អត្រាពន្ធ")
    taxable_amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="ចំនួនអាចពន្ធបាន")

    # Salary tax specific fields
    deduction_children = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="ការកាត់ពន្ធកូន")
    deduction_wife = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="ការកាត់ពន្ធប្រពន្ធ")
    total_deductions = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="ការកាត់ពន្ធសរុប")
    salary_tax_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="ពន្ធប្រាក់បៀវតន៏")
    grant_benefit_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="អត្ថប្រយោជន៍/អំណោយ")
    grant_tax_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="ពន្ធលើអត្ថប្រយោជន៍")

    # Property tax specific fields
    base_rate = models.DecimalField(max_digits=5, decimal_places=4, default=0, verbose_name="អត្រាគោល")
    property_type_multiplier = models.DecimalField(max_digits=3, decimal_places=2, default=1, verbose_name="គុណនាមប្រភេទអចលនទ្រព្យ")
    progressive_multiplier = models.DecimalField(max_digits=3, decimal_places=2, default=1, verbose_name="គុណនាមវឌ្ឍនភាព")
    final_rate = models.DecimalField(max_digits=5, decimal_places=4, default=0, verbose_name="អត្រាចុងក្រោយ")

    # Tax components breakdown (JSON field for flexible storage)
    tax_components = models.JSONField(default=dict, verbose_name="សមាសធាតុពន្ធ", help_text="JSON object containing detailed tax calculation components")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="កាលបរិច្ឆេទ")

    class Meta:
        verbose_name = "ព័ត៌មានលម្អិតនៃការគណនាពន្ធ"
        verbose_name_plural = "ព័ត៌មានលម្អិតនៃការគណនាពន្ធ"

    def __str__(self):
        return f"ព័ត៌មានលម្អិតការគណនា - {self.tax_record}"

    def get_tax_breakdown(self):
        """Returns a dictionary with the tax calculation breakdown"""
        breakdown = {
            'tax_rate': float(self.tax_rate),
            'taxable_amount': float(self.taxable_amount),
            'total_tax': float(self.salary_tax_amount + self.grant_tax_amount) if self.tax_record.tax_type == 'salary' else float(self.tax_record.tax_amount)
        }

        if self.tax_record.tax_type == 'salary':
            breakdown.update({
                'deductions': {
                    'children': float(self.deduction_children),
                    'wife': float(self.deduction_wife),
                    'total': float(self.total_deductions)
                },
                'tax_components': {
                    'salary_tax': float(self.salary_tax_amount),
                    'grant_tax': float(self.grant_tax_amount)
                }
            })
        else:  # property tax
            breakdown.update({
                'rate_calculation': {
                    'base_rate': float(self.base_rate),
                    'property_type_multiplier': float(self.property_type_multiplier),
                    'progressive_multiplier': float(self.progressive_multiplier),
                    'final_rate': float(self.final_rate)
                }
            })

        return breakdown