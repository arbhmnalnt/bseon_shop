from django.contrib import admin
from .models import Unit, Product, ProductUnit

# 🟩 واجهة إدارة وحدة (مطلوب للـ autocomplete)
class UnitAdmin(admin.ModelAdmin):
    search_fields = ['name']

# 🟩 عرض وحدات المنتج داخل المنتج نفسه
class ProductUnitInline(admin.TabularInline):
    model = ProductUnit
    extra = 1
    autocomplete_fields = ['unit']
    fields = ['unit', 'level', 'conversion_factor', 'cost_price', 'sell_price', 'quantity']

# 🟩 تخصيص واجهة المنتج
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductUnitInline]
    list_display = ['name', 'category']
    search_fields = ['name', 'category']

# 🟩 تسجيل الموديلات في لوحة التحكم
admin.site.register(Unit, UnitAdmin)
admin.site.register(Product, ProductAdmin)
