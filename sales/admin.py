from django.contrib import admin
from .models import Sale, SaleItem

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1
    autocomplete_fields = ['product_unit']
    fields = ['product_unit', 'quantity', 'price', 'line_total']

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display   = ['id', 'customer_name', 'date', 'total', 'status']
    list_filter    = ['date', 'status']
    search_fields  = ['customer_name']
    inlines        = [SaleItemInline]
