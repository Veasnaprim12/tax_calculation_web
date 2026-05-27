from django.contrib import admin
from .models import TaxRecord, TaxCalculationDetail


class TaxCalculationDetailInline(admin.StackedInline):
    model = TaxCalculationDetail
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('tax_rate', 'taxable_amount', 'total_deductions', 'salary_tax_amount', 'grant_tax_amount', 'final_rate', 'created_at')


@admin.register(TaxRecord)
class TaxRecordAdmin(admin.ModelAdmin):
    list_display = ('tax_type', 'income', 'tax_amount', 'currency', 'status', 'created_at')
    list_filter = ('tax_type', 'currency', 'status', 'wife_status', 'created_at')
    search_fields = ('tax_type', 'income')
    readonly_fields = ('created_at',)
    inlines = [TaxCalculationDetailInline]
    
    fieldsets = (
        ('ព័ត៌មានប្រាథមិក', {
            'fields': ('tax_type', 'currency', 'created_at')
        }),
        ('ចំណូល/តម្លៃអចលនទ្រព្យ', {
            'fields': ('income', 'property_value', 'property_type')
        }),
        ('ព័ត៌មានគ្រួសារ', {
            'fields': ('status', 'wife_status', 'dependents'),
            'classes': ('collapse',)
        }),
        ('លទ្ធផលគណនា', {
            'fields': ('tax_amount', 'net_income'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TaxCalculationDetail)
class TaxCalculationDetailAdmin(admin.ModelAdmin):
    list_display = ('tax_record', 'tax_rate', 'taxable_amount', 'salary_tax_amount', 'grant_tax_amount', 'final_rate')
    list_filter = ('tax_record__tax_type', 'created_at')
    search_fields = ('tax_record__tax_type',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('ឯកសារ', {
            'fields': ('tax_record',)
        }),
        ('អត្រាពន្ធ', {
            'fields': ('tax_rate', 'base_rate', 'final_rate')
        }),
        ('ចំនួនពន្ធ', {
            'fields': ('taxable_amount', 'salary_tax_amount', 'grant_tax_amount')
        }),
        ('ការកាត់ពន្ធ', {
            'fields': ('total_deductions', 'deduction_children', 'deduction_wife'),
            'classes': ('collapse',)
        }),
        ('គុណនាម', {
            'fields': ('property_type_multiplier', 'progressive_multiplier'),
            'classes': ('collapse',)
        }),
        ('ព័ត៌មានលម្អិត', {
            'fields': ('tax_components', 'created_at'),
            'classes': ('collapse',)
        }),
    )