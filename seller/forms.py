from django import forms
from .models import Invoice, InvoiceItem
from stock.models import Product, Unit

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
    unit = forms.ModelChoiceField(
        queryset=Unit.objects.all(),
        label="Unit",
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
        fields = ['product', 'unit', 'quantity', 'price_per_unit']
