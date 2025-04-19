from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum, F
from django.utils import timezone
from inventory.models import ProductUnit
from sales.models import Sale
from django.db.models.functions import TruncDay, TruncMonth
from purchases.models import Purchase

def revenue_today_api(request):
    today = timezone.localdate()
    total = Sale.objects.filter(date=today, status='final') \
                        .aggregate(sum=Sum('total'))['sum'] or 0
    return JsonResponse({'today': float(total)})

def revenue_by_day(request):
    # Group by day, summing totals
    qs = (
        Sale.objects
            .filter(status='final')
            .annotate(day=TruncDay('date'))
            .values('day')
            .annotate(total=Sum('total'))
            .order_by('day')
    )
    data = list(qs)  # [{'day': date(2025,4,19), 'total': 60.00}, ...]
    return render(request, 'reports/revenue_by_day.html', {'data': data})

def revenue_by_month(request):
    qs = (
        Sale.objects
            .filter(status='final')
            .annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(total=Sum('total'))
            .order_by('month')
    )
    data = list(qs)  # now month is a datetime.date(YYYY, MM, 1)
    return render(request, 'reports/revenue_by_month.html', {'data': data})

def top_products(request):
    # sum of sales per product unit, then group by product name
    qs = (
      Sale.objects.filter(status='final')
      .values(name=F('items__product_unit__product__name'))
      .annotate(revenue=Sum('items__line_total'))
      .order_by('-revenue')[:10]
    )
    return render(request, 'reports/top_products.html', {'data': qs})

def low_stock_alerts(request):
    # any ProductUnit under threshold (e.g. < 10)
    threshold = 10
    qs = ProductUnit.objects.filter(quantity__lt=threshold) \
         .select_related('product','unit') \
         .order_by('quantity')
    return render(request, 'reports/low_stock.html', {
      'data': qs,
      'threshold': threshold
    })
