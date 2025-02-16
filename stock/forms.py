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
        widgets = {
            'base_unit': Select2TagWidget(
                attrs={
                    'data-tags': 'true',
                    'data-placeholder': 'Select or add a base unit',
                    'data-width': '100%'
                }
            ),
            'big_unit': Select2TagWidget(
                attrs={
                    'data-tags': 'true',
                    'data-placeholder': 'Select or add a big unit',
                    'data-width': '100%'
                }
            ),
        }
