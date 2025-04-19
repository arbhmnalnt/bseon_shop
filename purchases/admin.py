from django.contrib import admin
from .models import Purchase, PurchaseItem

class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1
    autocomplete_fields = ['product_unit']
    fields = ['product_unit', 'quantity', 'price', 'line_total']

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display    = ['id', 'supplier', 'date', 'total']
    list_filter     = ['date', 'supplier']
    search_fields   = ['supplier__name']
    inlines         = [PurchaseItemInline]
