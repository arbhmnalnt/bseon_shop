from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'supplier', 'price', 'stock_quantity', 'barcode')  # Fields displayed in the list view
    search_fields = ('name', 'category', 'supplier', 'barcode')  # Enables search bar
    list_filter = ('category', 'supplier')  # Adds filter options
    ordering = ('name',)
