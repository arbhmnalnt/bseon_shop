from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'  # Include all fields
        labels = {
            'name': 'اسم المنتج',
            'category': 'التصنيف - اختيارى',
            'supplier': 'المورد - اختيارى',
            'price': 'السعر',
            'stock_quantity': 'الكمية بالمخزن',
            'barcode': 'الباركود - اختيارى',
        }