from django import forms
from .models import Invoice, InvoiceItem
from stock.models import Product

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['customer_name']

class InvoiceItemForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        label="المنتج",
        widget=forms.Select(attrs={'class': 'form-control select-product'})
    )
    sold_unit = forms.ChoiceField(
        choices=InvoiceItem.UNIT_CHOICES,
        label="وحدة البيع",
        widget=forms.Select(attrs={'class': 'form-control unit-select'})
    )
    # Render price_per_unit as read-only; it will be set via JavaScript based on the selected unit.
    price_per_unit = forms.DecimalField(
        widget=forms.TextInput(attrs={'class': 'form-control price-field', 'readonly': 'readonly'})
    )
    class Meta:
        model = InvoiceItem
        fields = ['product', 'quantity', 'sold_unit', 'price_per_unit']
