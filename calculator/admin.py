from django.contrib import admin
from .models import TaxRecord, TaxCalculationDetail

admin.site.register(TaxRecord)
admin.site.register(TaxCalculationDetail)