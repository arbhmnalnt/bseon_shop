from django import forms
from .models import Product, ProductUnit

class ProductForm(forms.ModelForm):
    class Meta:
        model  = Product
        fields = ['name', 'category', 'description', 'supplier']  # ← include supplier
        labels = {
            'name':        'اسم المنتج',
            'category':    'التصنيف',
            'description': 'الوصف',
            'supplier':    'المورد',
        }
        widgets = {
            'name':        forms.TextInput(attrs={'class': 'form-control'}),
            'category':    forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows':3}),
            'supplier':    forms.Select(attrs={'class': 'form-control'}),  # ← styled select
        }

class ProductUnitForm(forms.ModelForm):
    class Meta:
        model = ProductUnit
        fields = [
            'product', 'unit', 'level', 'conversion_factor',
            'cost_price', 'price_1', 'price_2', 'price_3', 'quantity'
        ]
        labels = {
            'product': 'المنتج',
            'unit': 'الوحدة',
            'level': 'المستوى (1 = الأكبر)',
            'conversion_factor': 'عدد الوحدات الأقل داخل هذه الوحدة',
            'cost_price': 'سعر التكلفة',
            'price_1': 'السعر 1 (أساسي)',
            'price_2': 'السعر 2 (عرض)',
            'price_3': 'السعر 3 (VIP)',
            'quantity': 'الكمية المتاحة',
        }
        widgets = {
            field: forms.NumberInput(attrs={'class': 'form-control'})
            for field in ['level', 'conversion_factor', 'cost_price', 'price_1', 'price_2', 'price_3', 'quantity']
        }
        widgets['product'] = forms.Select(attrs={'class': 'form-control'})
        widgets['unit'] = forms.Select(attrs={'class': 'form-control'})