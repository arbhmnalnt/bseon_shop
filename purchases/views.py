from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Purchase
from .forms import PurchaseForm, PurchaseItemFormSet

def purchase_list(request):
    purchases = Purchase.objects.select_related('supplier').all().order_by('-date')
    return render(request, 'purchases/purchase_list.html', {'purchases': purchases})

def purchase_detail(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    return render(request, 'purchases/purchase_detail.html', {'purchase': purchase})

def purchase_create(request):
    if request.method == 'POST':
        form    = PurchaseForm(request.POST)
        formset = PurchaseItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            purchase = form.save(commit=False)
            purchase.total = 0
            purchase.save()
            formset.instance = purchase
            items = formset.save()
            # recalc total
            total = sum(item.line_total for item in items)
            purchase.total = total
            purchase.save()
            messages.success(request, "تم إنشاء فاتورة الشراء بنجاح.")
            return redirect('purchase_detail', pk=purchase.pk)
    else:
        form    = PurchaseForm()
        formset = PurchaseItemFormSet()
    return render(request, 'purchases/purchase_form.html', {
        'form': form, 'formset': formset
    })

def purchase_edit(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    if request.method == 'POST':
        form    = PurchaseForm(request.POST, instance=purchase)
        formset = PurchaseItemFormSet(request.POST, instance=purchase)
        if form.is_valid() and formset.is_valid():
            purchase = form.save(commit=False)
            purchase.total = 0
            purchase.save()
            items = formset.save()
            total = sum(item.line_total for item in items)
            purchase.total = total
            purchase.save()
            messages.success(request, "تم تحديث فاتورة الشراء.")
            return redirect('purchase_detail', pk=pk)
    else:
        form    = PurchaseForm(instance=purchase)
        formset = PurchaseItemFormSet(instance=purchase)
    return render(request, 'purchases/purchase_form.html', {
        'form': form, 'formset': formset, 'purchase': purchase
    })

def purchase_delete(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    if request.method == 'POST':
        purchase.delete()
        messages.success(request, "تم حذف فاتورة الشراء.")
        return redirect('purchase_list')
    return render(request, 'purchases/purchase_confirm_delete.html', {'purchase': purchase})
