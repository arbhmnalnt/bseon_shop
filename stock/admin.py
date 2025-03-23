from django.contrib import admin
from .models import Unit, Product, ProductUnit

class ProductUnitInline(admin.TabularInline):
    model = ProductUnit
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'supplier', 'kind', 'base_unit')
    inlines = [ProductUnitInline]

admin.site.register(Unit)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductUnit)
