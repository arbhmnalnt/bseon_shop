from django.urls import path
from .views import *

app_name = "stock"

urlpatterns = [
    path('products/', product_list, name='product_list'),
    path('products/add/', product_create, name='product_create'),
    path('products/edit/<int:pk>/', product_update, name='product_update'),
    path('products/delete/<int:pk>/', product_delete, name='product_delete'),
    # path('stock/', views.stock_list, name='stock_list'),
    # path('stock/add/', views.stock_create, name='stock_create'),
]