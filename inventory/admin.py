from django.contrib import admin
from .models import Unit, Product, ProductUnit

class ProductUnitInline(admin.TabularInline):
    model = ProductUnit
    extra = 1
    autocomplete_fields = ['unit']
    fields = [
        'unit', 'level', 'conversion_factor',
        'cost_price', 'price_1', 'price_2', 'price_3', 'quantity'
    ]

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductUnitInline]
    list_display = ['name', 'category']
    search_fields = ['name', 'category']

class UnitAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(Unit, UnitAdmin)
admin.site.register(Product, ProductAdmin)
