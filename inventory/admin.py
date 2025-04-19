from django.contrib import admin
from .models import Unit, Product, ProductUnit

# 1) Register Unit with search_fields for autocomplete
@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    search_fields = ['name']

# 2) Inline for ProductUnit on the Product admin
class ProductUnitInline(admin.TabularInline):
    model = ProductUnit
    extra = 1
    autocomplete_fields = ['unit']       # now works, since Unit has search_fields
    fields = ['unit', 'level', 'conversion_factor', 'cost_price', 'sell_price', 'quantity']

# 3) Product admin with inline
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductUnitInline]
    list_display = ['name', 'category']
    search_fields = ['name', 'category']

# (Optional) If you want a standalone ProductUnit admin with autocomplete too:
@admin.register(ProductUnit)
class ProductUnitAdmin(admin.ModelAdmin):
    autocomplete_fields = ['unit', 'product']
    search_fields = ['product__name', 'unit__name']
