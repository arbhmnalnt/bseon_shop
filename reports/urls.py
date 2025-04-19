from django.urls import path
from . import views

urlpatterns = [
    path('revenue/today/',     views.revenue_today_api,  name='revenue_today_api'),
    path('revenue/daily/',     views.revenue_by_day,     name='revenue_by_day'),
    path('revenue/monthly/',   views.revenue_by_month,   name='revenue_by_month'),
    path('top-products/',      views.top_products,       name='top_products'),
    path('low-stock/',         views.low_stock_alerts,   name='low_stock'),
]
