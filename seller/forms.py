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
        label="Product",
        widget=forms.Select(attrs={'class': 'form-control select-product'})
    )
    # Render the price field and make it read-only
    price_per_unit = forms.DecimalField(
        widget=forms.TextInput(attrs={'class': 'form-control price-field', 'readonly': 'readonly'})
    )
    class Meta:
        model = InvoiceItem
        fields = ['product', 'quantity', 'price_per_unit']
