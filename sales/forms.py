from django import forms
from django.forms.models import inlineformset_factory
from inventory.models import ProductUnit
from .models import Sale, SaleItem

class ProductUnitChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        """
        Display each option as:
          ProductName — UnitName (رصيد: quantity)
        """
        return f"{obj.product.name} — {obj.unit.name} (رصيد: {obj.quantity})"


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
    PRICE_CHOICES = [
        ('price_1', 'السعر 1 (افتراضي)'),
        ('price_2', 'السعر 2 (عرض)'),
        ('price_3', 'السعر 3 (VIP)'),
    ]

    product_unit = ProductUnitChoiceField(
        queryset=ProductUnit.objects.select_related('product', 'unit'),
        widget=forms.Select(attrs={'class': 'form-control js-select2 product-unit'}),
        empty_label="اختر منتجاً"
    )

    price_type = forms.ChoiceField(
        choices=PRICE_CHOICES,
        label="نوع السعر",
        widget=forms.Select(attrs={'class': 'form-select price-type'})
    )

    class Meta:
        model = SaleItem
        fields = ['product_unit', 'price_type', 'quantity', 'unit_price']
        labels = {
            'product_unit': 'المنتج',
            'price_type': 'نوع السعر',
            'quantity': 'الكمية',
            'unit_price': 'سعر الوحدة المختار',
        }
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control qty-input', 'min': 0, 'step': 'any'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control unit-price-input', 'readonly': 'readonly'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        unit = cleaned_data.get('product_unit')
        price_type = cleaned_data.get('price_type')

        if unit and price_type:
            selected_price = getattr(unit, price_type, None)
            if selected_price is not None:
                cleaned_data['unit_price'] = selected_price
                cleaned_data['line_total'] = selected_price * cleaned_data.get('quantity', 0)
            else:
                raise forms.ValidationError("السعر المختار غير متاح لهذا المنتج.")
        return cleaned_data


SaleItemFormSet = inlineformset_factory(
    Sale,
    SaleItem,
    form=SaleItemForm,
    extra=1,
    can_delete=True,
)
