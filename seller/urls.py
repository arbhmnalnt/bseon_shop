from django.urls import path
from .views import create_invoice, invoice_list, invoice_detail, get_product_price

app_name = 'seller'

urlpatterns = [
    path('create/', create_invoice, name='invoice-create'),
    path('invoices/', invoice_list, name='invoice-list'),
    path('invoice/<int:invoice_id>/', invoice_detail, name='invoice-detail'),
    path('get-product-price/<int:product_id>/', get_product_price, name='get-product-price'),
]
