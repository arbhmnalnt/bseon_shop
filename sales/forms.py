# sales/forms.py

from django import forms
from django.forms.models import inlineformset_factory
from inventory.models import ProductUnit
from .models import Sale, SaleItem

class ProductUnitChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        """
        Display each option as:
          ProductName — UnitName (رصيد: quantity, سعر: sell_price)
        """
        return f"{obj.product.name} — {obj.unit.name} (رصيد: {obj.quantity}, سعر: {obj.sell_price})"

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer_name', 'status']
        labels = {
            'customer_name': 'اسم العميل',
            'status':        'الحالة',
        }
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'status':        forms.Select(attrs={'class': 'form-control'}),
        }

class SaleItemForm(forms.ModelForm):
    product_unit = ProductUnitChoiceField(
        queryset=ProductUnit.objects.select_related('product','unit'),
        widget=forms.Select(attrs={'class': 'form-control js-select2'}),
        empty_label="اختر منتجاً"
    )

    class Meta:
        model  = SaleItem
        fields = ['product_unit', 'quantity', 'price']
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control qty-input', 'min': 0, 'step': 'any'}),
            'price':    forms.NumberInput(attrs={'class': 'form-control price-input', 'min': 0, 'step': 'any'}),
        }

SaleItemFormSet = inlineformset_factory(
    Sale,
    SaleItem,
    form=SaleItemForm,
    extra=1,
    can_delete=True,
    # The quantity & price widgets are already defined on SaleItemForm, 
    # but if you need additional customization you can override here.
)
