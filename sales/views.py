from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Sale
from .forms import SaleForm, SaleItemFormSet
from inventory.models import ProductUnit
from django.db import transaction
from django.http import JsonResponse
from .forms import SaleForm, SaleItemFormSet




def get_price(request, unit_id, price_type):
    try:
        unit = ProductUnit.objects.get(pk=unit_id)
        price = getattr(unit, price_type)
        return JsonResponse({'price': float(price)})
    except ProductUnit.DoesNotExist:
        return JsonResponse({'error': 'Product Unit not found'}, status=404)

def sale_list(request):
    sales = Sale.objects.all().order_by('-date')
    return render(request, 'sales/sale_list.html', {'sales': sales})

def sale_detail(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    return render(request, 'sales/sale_detail.html', {'sale': sale})

def sale_create(request):
    if request.method == 'POST':
        sale_form = SaleForm(request.POST)
        formset = SaleItemFormSet(request.POST)

        if sale_form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    sale = sale_form.save(commit=False)
                    sale.total = 0
                    sale.save()

                    total = 0
                    for form in formset:
                        if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                            item = form.save(commit=False)
                            item.sale = sale
                            item.unit_price = form.cleaned_data['unit_price']
                            item.line_total = form.cleaned_data['line_total']
                            item.save()
                            total += item.line_total

                    sale.total = total
                    sale.save()

                    messages.success(request, '✅ تم حفظ الفاتورة بنجاح.')
                    return redirect('sale_list')
            except Exception as e:
                messages.error(request, f'حدث خطأ أثناء حفظ الفاتورة: {str(e)}')
        else:
            messages.error(request, '❌ هناك أخطاء في البيانات، برجاء مراجعتها.')
    else:
        sale_form = SaleForm()
        formset = SaleItemFormSet()

    return render(request, 'sales/sale_form.html', {   # ✅ تأكدنا إنه sale_create.html
        'form': sale_form,
        'formset': formset,
    })

def sale_edit(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        form    = SaleForm(request.POST, instance=sale)
        # formset = SaleItemFormSet(request.POST, instance=sale)
        formset = SaleItemFormSet(request.POST, instance=sale)

        if form.is_valid() and formset.is_valid():
            sale = form.save(commit=False)
            sale.total = 0
            sale.save()
            items = formset.save()
            total = sum(item.line_total for item in items)
            sale.total = total
            sale.save()
            messages.success(request, "تم تحديث فاتورة البيع.")
            return redirect('sale_detail', pk=pk)
    else:
        form    = SaleForm(instance=sale)
        formset = SaleItemFormSet(instance=sale)
    product_units = ProductUnit.objects.select_related('product','unit')
    price_map = {pu.id: float(pu.price_1    ) for pu in product_units}
    stock_map = {pu.id: float(pu.quantity)   for pu in product_units}
    return render(request, 'sales/sale_form.html', {
        'form': form, 'formset': formset, 'sale': None,
        'price_map': price_map, 'stock_map': stock_map
    })

def sale_delete(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        sale.delete()
        messages.success(request, "تم حذف فاتورة البيع.")
        return redirect('sale_list')
    return render(request, 'sales/sale_confirm_delete.html', {'sale': sale})
