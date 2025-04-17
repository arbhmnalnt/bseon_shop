from django import forms
from .models import Product, ProductUnit

# 🟢 نموذج إضافة منتج جديد
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description']
        labels = {
            'name': 'اسم المنتج',
            'category': 'التصنيف',
            'description': 'الوصف',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# 🟢 نموذج إضافة وحدة منتج جديدة
class ProductUnitForm(forms.ModelForm):
    class Meta:
        model = ProductUnit
        fields = ['product', 'unit', 'level', 'conversion_factor', 'cost_price', 'sell_price', 'quantity']
        labels = {
            'product': 'المنتج',
            'unit': 'الوحدة',
            'level': 'المستوى (1 للأكبر)',
            'conversion_factor': 'عدد الوحدات الأقل',
            'cost_price': 'سعر التكلفة',
            'sell_price': 'سعر البيع',
            'quantity': 'الكمية المتاحة',
        }
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'level': forms.NumberInput(attrs={'class': 'form-control'}),
            'conversion_factor': forms.NumberInput(attrs={'class': 'form-control'}),
            'cost_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'sell_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }
