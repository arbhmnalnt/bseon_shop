from django import forms
from.models import Product, StockEntry

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        labels = {
            'name': "اسم المنتج",
            'category': "التصنيف",
            'supplier': "المورد",
            'big_unit': "الوحدة الكبيرة",
            'big_unit_cost_price': "سعر التكلفة للوحدة الكبيرة",
            'big_unit_sell_price': "سعر البيع للوحدة الكبيرة",
            'small_unit': "الوحدة الصغيرة",
            'small_units_counts': "عدد الوحدات الصغيرة في الكبيرة",
            'small_unit_cost_price': "سعر التكلفة للوحدة الصغيرة",
            'small_unit_sell_price': "سعر البيع للوحدة الصغيرة",
            'stock_quantity_big': "الكمية ",
            'barcode': "الباركود",
        }

class StockEntryForm(forms.ModelForm):
    class Meta:
        model = StockEntry
        fields = '__all__'
        labels = {
            'product': "المنتج",
            'quantity': "الكمية",
            'unit': "الوحدة",
            'transaction_type': "نوع العملية",
            'date': "التاريخ",
        }