from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'base_unit', 'big_unit', 'units_in_big_unit',
        'buy_price_big', 'sell_price_base', 'stock_quantity', 'barcode'
    )
    fields = (
        'name', 'category', 'supplier',
        'base_unit', 'big_unit', 'units_in_big_unit',
        'buy_price_big', 'sell_price_base',
        'stock_quantity', 'barcode'
    )
