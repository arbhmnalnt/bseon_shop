from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Unit, Product, StockEntry
from .forms import *



@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    form = ProductForm
    list_display = ('name', 'category', 'supplier', 'big_unit', 'small_unit', 'stock_quantity_big', 'barcode')
    search_fields = ('name', 'category', 'supplier', 'barcode')
    list_filter = ('category', 'supplier')
    
    fieldsets = (
        ("Product Info", {"fields": ("name", "category", "supplier", "barcode")}),
        ("Unit & Pricing", {"fields": ("big_unit", "big_unit_cost_price", "big_unit_sell_price",
                                       "small_unit", "small_units_counts", 
                                       "small_unit_cost_price", "small_unit_sell_price")}),
        ("Stock Information", {"fields": ("stock_quantity_big",)}),
    )

@admin.register(StockEntry)
class StockEntryAdmin(admin.ModelAdmin):
    list_display = ('product', 'unit', 'quantity', 'transaction_type', 'created_at')
    search_fields = ('product__name',)
    list_filter = ('transaction_type', 'created_at')
    ordering = ('-created_at',)

