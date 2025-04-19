from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Sale
from .forms import SaleForm, SaleItemFormSet
from inventory.models import ProductUnit



def sale_list(request):
    sales = Sale.objects.all().order_by('-date')
    return render(request, 'sales/sale_list.html', {'sales': sales})

def sale_detail(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    return render(request, 'sales/sale_detail.html', {'sale': sale})

def sale_create(request):
    if request.method == 'POST':
        form    = SaleForm(request.POST)
        formset = SaleItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            sale = form.save(commit=False)
            sale.total = 0
            sale.save()
            formset.instance = sale
            items = formset.save()
            total = sum(item.line_total for item in items)
            sale.total = total
            sale.save()
            messages.success(request, "تم إنشاء فاتورة البيع بنجاح.")
            return redirect('sale_detail', pk=sale.pk)
    else:
        form    = SaleForm()
        formset = SaleItemFormSet()
    product_units = ProductUnit.objects.select_related('product','unit')
    price_map = {pu.id: float(pu.sell_price) for pu in product_units}
    stock_map = {pu.id: float(pu.quantity)   for pu in product_units}
    return render(request, 'sales/sale_form.html', {
        'form': form, 'formset': formset, 'sale': None,
        'price_map': price_map, 'stock_map': stock_map
    })

def sale_edit(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == 'POST':
        form    = SaleForm(request.POST, instance=sale)
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
    price_map = {pu.id: float(pu.sell_price) for pu in product_units}
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
