from django.db import models


class TaxRecord(models.Model):
    TAX_TYPE_CHOICES = [
        ('salary', 'ពន្ធលើប្រាក់បៀវតន៏'),
        ('property', 'ពន្ធអាក'),
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

    tax_type = models.CharField(max_length=10, choices=TAX_TYPE_CHOICES, default='salary', verbose_name="ប្រភេទពន្ធ")
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='KHR', verbose_name="រូបិយប័ណ្ណ")
    income = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="ចំណូល/តម្លៃអចលនទ្រព្យ")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name="ស្ថានភាពគ្រួសារ", blank=True, null=True)
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
        else:
            return f"ពន្ធអាក: {self.property_value:,}៛ → ពន្ធ: {self.tax_amount:,}៛ (ថ្ងៃ {self.created_at.date()})"