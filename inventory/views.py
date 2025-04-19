# inventory/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, ProductUnit
from .forms import ProductForm, ProductUnitForm

# عرض قائمة المنتجات
def product_list(request):
    products = Product.objects.all()
    return render(request, 'inventory/product_list.html', {'products': products})

# عرض تفاصيل منتج
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'inventory/product_detail.html', {'product': product})

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
    if request.method == 'POST':
        product_id = unit.product.id
        unit.delete()
        messages.success(request, "تم حذف الوحدة.")
        return redirect('product_detail', pk=product_id)
    return render(request, 'inventory/delete_product_unit.html', {'unit': unit})
