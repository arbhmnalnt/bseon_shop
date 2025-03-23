from django import forms
from .models import Unit, Product, ProductUnit

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['name']
        labels = {'name': "اسم الوحدة"}

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'base_unit', 'supplier', 'kind']
        labels = {
            'name': "اسم المنتج",
            'base_unit': "الوحدة الأساسية",
            'supplier': "المورد",
            'kind': "التصنيف"
        }

class ProductUnitForm(forms.ModelForm):
    class Meta:
        model = ProductUnit
        fields = ['unit', 'level', 'conversion_factor', 'cost_price', 'sell_price']
        labels = {
            'unit': "الوحدة",
            'level': "المستوى",
            'conversion_factor': "عامل التحويل",
            'cost_price': "سعر التكلفة",
            'sell_price': "سعر البيع",
        }
