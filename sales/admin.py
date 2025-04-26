from django.contrib import admin
from .models import Sale, SaleItem, ProductUnit

@admin.register(ProductUnit)
class ProductUnitAdmin(admin.ModelAdmin):
    search_fields = ['product__name', 'unit__name']
    list_display = ['product', 'unit', 'level', 'quantity']

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1
    autocomplete_fields = ['product_unit']
    fields = ['product_unit', 'quantity', 'unit_price', 'line_total']
    readonly_fields = ['line_total']

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display   = ['id', 'customer_name', 'date', 'total', 'status']
    list_filter    = ['date', 'status']
    search_fields  = ['customer_name']
    inlines        = [SaleItemInline]
