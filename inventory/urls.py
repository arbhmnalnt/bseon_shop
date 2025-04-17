from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/create/', views.product_create, name='product_create'),

    # ✅ المسار المطلوب لإضافة وحدة منتج:
    path('product-unit/add/', views.add_product_unit, name='add_product_unit'),
    path('product-unit/add/<int:product_id>/', views.add_product_unit, name='add_product_unit_for_product'),
]
