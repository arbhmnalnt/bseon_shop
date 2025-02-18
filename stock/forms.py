from django import forms
from .models import Product
from django_select2.forms import Select2TagWidget

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'category',
            'supplier',
            'base_unit',
            'big_unit',
            'units_in_big_unit',
            'buy_price_big',
            'sell_price_base',
            'stock_quantity',
            'barcode'
        ]
