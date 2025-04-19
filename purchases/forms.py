from django import forms
from .models import Purchase, PurchaseItem
from django.forms.models import inlineformset_factory

class PurchaseForm(forms.ModelForm):
    class Meta:
        model  = Purchase
        fields = ['supplier', 'notes']
        labels = {
            'supplier': 'المورد',
            'notes':    'ملاحظات',
        }
        widgets = {
            'supplier': forms.Select(attrs={'class':'form-control'}),
            'notes':    forms.Textarea(attrs={'class':'form-control', 'rows':2}),
        }

# Inline formset for items
PurchaseItemFormSet = inlineformset_factory(
    Purchase,
    PurchaseItem,
    fields=('product_unit','quantity','price'),
    extra=1,
    can_delete=True,
    widgets={
      'product_unit': forms.Select(attrs={'class':'form-control js-select2'}),
      'quantity':     forms.NumberInput(attrs={'class':'form-control','min':0,'step':'any'}),
      'price':        forms.NumberInput(attrs={'class':'form-control','min':0,'step':'any'}),
    }
)
