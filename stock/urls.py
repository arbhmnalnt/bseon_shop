from django.urls import path
from .views import *

app_name = "stock"

urlpatterns = [
    path('', product_list, name='product_list'),
    path('new/', product_create, name='product_create'),
    path('<int:pk>/edit/', product_update, name='product_update'),
    # path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
]
