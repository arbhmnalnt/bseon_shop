from django import forms
from .models import Invoice, InvoiceItem
from stock.models import Product, ProductUnit

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['customer_name']
        labels = {
            'customer_name': "اسم العميل"
        }

class InvoiceItemForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        label="المنتج",
        widget=forms.Select(attrs={'class': 'form-control select-product'})
    )
    # This field will be populated dynamically based on the selected product.
    product_unit = forms.ModelChoiceField(
        queryset=ProductUnit.objects.none(),
        label="الوحدة",
        widget=forms.Select(attrs={'class': 'form-control select-unit'})
    )
    quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control quantity-field', 'min': 1})
    )
    price_per_unit = forms.DecimalField(
        widget=forms.TextInput(attrs={'class': 'form-control price-field', 'readonly': 'readonly'})
    )

    class Meta:
        model = InvoiceItem
        # Include 'id' so that existing items are recognized during updates.
        fields = ['id', 'product', 'product_unit', 'quantity', 'price_per_unit']
        widgets = {
            'id': forms.HiddenInput()
        }
