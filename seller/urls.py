from django.urls import path
from .views import *

app_name = 'seller'

urlpatterns = [
    path('create/', create_invoice, name='invoice-create'),
    path('invoices/', invoice_list, name='invoice-list'),
    path('invoice/<int:invoice_id>/', invoice_detail, name='invoice-detail'),
    path('get_product_price/', get_product_price, name='get_product_price'),


]
