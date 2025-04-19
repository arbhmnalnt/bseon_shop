from django.urls import path
from . import views

urlpatterns = [
    path('',                               views.product_list,               name='product_list'),
    path('product/create/',                views.product_create,             name='product_create'),
    path('product/<int:pk>/',              views.product_detail,             name='product_detail'),
    path('product/<int:pk>/edit/',         views.product_edit,               name='product_edit'),
    # Product Units (add / edit / delete)
    path('product-unit/add/',             views.add_product_unit,           name='add_product_unit'),
    path('product-unit/add/<int:product_id>/', 
                                         views.add_product_unit,           name='add_product_unit_for_product'),
    path('product-unit/<int:pk>/edit/',   views.edit_product_unit,          name='edit_product_unit'),
    path('product-unit/<int:pk>/delete/', views.delete_product_unit,        name='delete_product_unit'),
]
