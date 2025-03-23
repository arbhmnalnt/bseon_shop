from django.urls import path
from .views import *

app_name = 'seller'

urlpatterns = [
    path('invoices/', invoice_list, name='invoice_list'),
    path('create/', invoice_create, name='invoice_create'),
    path('update/<int:pk>/', invoice_update, name='invoice_update'),
    path('delete/<int:pk>/', invoice_delete, name='invoice_delete'),
    path('detail/<int:pk>/', invoice_detail, name='invoice_detail'),
    path('get_product_units/', get_product_units, name='get_product_units'),
    path('get_product_price/', get_product_price, name='get_product_price'),
]