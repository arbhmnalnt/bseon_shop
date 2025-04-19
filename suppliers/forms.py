from django import forms
from .models import Supplier

class SupplierForm(forms.ModelForm):
    class Meta:
        model  = Supplier
        fields = ['name', 'phone', 'email', 'address']
        labels = {
            'name':    'اسم المورد',
            'phone':   'رقم الهاتف',
            'email':   'البريد الإلكتروني',
            'address': 'العنوان',
        }
        widgets = {
            'name':    forms.TextInput(attrs={'class': 'form-control'}),
            'phone':   forms.TextInput(attrs={'class': 'form-control'}),
            'email':   forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
