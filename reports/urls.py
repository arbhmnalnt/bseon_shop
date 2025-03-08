from django.urls import path
from .views import *

app_name = 'reports'

urlpatterns = [
    path('', reports_home, name='home'),  # Main reports page
    # path('sales/', sales_report, name='sales_report'),
    # path('inventory/', inventory_report, name='inventory_report'),
    # path('profit/', profit_report, name='profit_report'),
    # path('customer/', customer_report, name='customer_report'),
    # path('supplier/', supplier_report, name='supplier_report'),
    # path('product/', product_report, name='product_report'),
]
