from django import forms
from .models import Sale, SaleItem
from django.forms.models import inlineformset_factory

class SaleForm(forms.ModelForm):
    class Meta:
        model  = Sale
        fields = ['customer_name', 'status']
        labels = {
            'customer_name': 'اسم العميل',
            'status':        'الحالة',
        }
        widgets = {
            'customer_name': forms.TextInput(attrs={'class':'form-control'}),
            'status':        forms.Select(attrs={'class':'form-control'}),
        }

SaleItemFormSet = inlineformset_factory(
    Sale,
    SaleItem,
    fields=('product_unit','quantity','price'),
    extra=1,
    can_delete=True,
    widgets={
      'product_unit': forms.Select(attrs={'class':'form-control js-select2'}),
      'quantity':     forms.NumberInput(attrs={'class':'form-control','min':0,'step':'any'}),
      'price':        forms.NumberInput(attrs={'class':'form-control','min':0,'step':'any'}),
    }
)
