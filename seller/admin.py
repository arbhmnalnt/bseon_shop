from django.contrib import admin
from report_builder.admin import ReportAdmin  # Using ReportAdmin for report-builder functionality
from .models import Invoice, InvoiceItem

@admin.register(Invoice)
class InvoiceAdmin(ReportAdmin, admin.ModelAdmin):
    # Override default fields inherited from ReportAdmin
    readonly_fields = ()  
    list_filter = ('created_at',)  # Only include fields present in the model
    list_display = ('id', 'customer_name', 'total_price', 'created_at')
    search_fields = ('id', 'customer_name')

@admin.register(InvoiceItem)
class InvoiceItemAdmin(ReportAdmin, admin.ModelAdmin):
    readonly_fields = ()
    list_filter = ()  # Remove default filters not applicable to InvoiceItem
    list_display = ('invoice', 'product', 'quantity', 'price_per_unit', 'total_price')
