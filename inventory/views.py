# inventory/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import ProtectedError

from .models import Product, ProductUnit
from .forms import ProductForm, ProductUnitForm
from purchases.models import PurchaseItem
from sales.models import SaleItem

# عرض قائمة المنتجات
def product_list(request):
    # prefetch units so we can sum quantities
    products = Product.objects.prefetch_related('units').all()
    # attach a total_quantity attribute to each product
    for p in products:
        p.total_quantity = sum(u.quantity for u in p.units.all())
    return render(request, 'inventory/product_list.html', {'products': products})

# عرض تفاصيل منتج
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    # all purchase items for any unit of this product
    purchase_history = (
        PurchaseItem.objects
        .filter(product_unit__product=product)
        .select_related('purchase', 'product_unit')
        .order_by('-purchase__date')
    )
    # all sale items for any unit of this product
    sale_history = (
        SaleItem.objects
        .filter(product_unit__product=product)
        .select_related('sale', 'product_unit')
        .order_by('-sale__date')
    )
    return render(request, 'inventory/product_detail.html', {
        'product': product,
        'purchase_history': purchase_history,
        'sale_history': sale_history,
    })

# إنشاء منتج جديد ثم تحويل لإضافة وحدات له
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            new_product = form.save()
            return redirect('add_product_unit_for_product', product_id=new_product.id)
    else:
        form = ProductForm()
    return render(request, 'inventory/product_form.html', {'form': form})

# تعديل بيانات المنتج
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تحديث المنتج بنجاح.")
            return redirect('product_detail', pk=pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'inventory/product_form.html', {'form': form})

# إضافة وحدة جديدة لأي منتج (إما عام أو محدد)
def add_product_unit(request, product_id=None):
    initial = {'product': product_id} if product_id else {}
    if request.method == 'POST':
        form = ProductUnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=form.cleaned_data['product'].id)
    else:
        form = ProductUnitForm(initial=initial)
    return render(request, 'inventory/add_product_unit.html', {'form': form})

# ✏️ تعديل وحدة منتج
def edit_product_unit(request, pk):
    unit = get_object_or_404(ProductUnit, pk=pk)
    if request.method == 'POST':
        form = ProductUnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تعديل الوحدة بنجاح.")
            return redirect('product_detail', pk=unit.product.id)
    else:
        form = ProductUnitForm(instance=unit)
    return render(request, 'inventory/edit_product_unit.html', {
        'form': form,
        'unit': unit,
    })

# 🗑️ حذف وحدة منتج
def delete_product_unit(request, pk):
    unit = get_object_or_404(ProductUnit, pk=pk)
    product_id = unit.product.id

    if request.method == 'POST':
        try:
            unit.delete()
            messages.success(request, 'تم حذف الوحدة بنجاح.')
        except ProtectedError:
            messages.error(request, 'لا يمكن حذف هذه الوحدة لأنها مستخدمة في عمليات بيع أو شراء.')

        return redirect('product_detail', product_id)

    return render(request, 'inventory/delete_product_unit.html', {'unit': unit})