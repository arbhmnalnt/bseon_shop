from django.contrib import admin
from .models import Invoice, InvoiceItem

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1  # Shows an empty row for quick product entry

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'total_price', 'created_at')
    search_fields = ('id', 'customer_name')
    list_filter = ('created_at',)
    inlines = [InvoiceItemInline]  # Allows adding items inside the Invoice admin page

@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'product', 'quantity', 'price_per_unit', 'total_price')
