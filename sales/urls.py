from django.urls import path
from . import views

urlpatterns = [
    path('',              views.sale_list,   name='sale_list'),
    path('create/',       views.sale_create, name='sale_create'),
    path('<int:pk>/',     views.sale_detail, name='sale_detail'),
    path('<int:pk>/edit/',views.sale_edit,   name='sale_edit'),
    path('<int:pk>/delete/',views.sale_delete,name='sale_delete'),
    path('ajax/get-price/<int:unit_id>/<str:price_type>/', views.get_price, name='ajax_get_price'),
]
