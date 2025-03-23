from django.shortcuts import render, get_object_or_404, redirect
from django.forms import inlineformset_factory
from .models import Product, Unit, ProductUnit
from .forms import ProductForm, ProductUnitForm, UnitForm

# --- Product Views ---

def product_list(request):
    products = Product.objects.all()
    return render(request, 'stock/product_list.html', {'products': products})

def product_create(request):
    ProductUnitFormSet = inlineformset_factory(Product, ProductUnit, form=ProductUnitForm, extra=1, can_delete=True)
    if request.method == "POST":
        form = ProductForm(request.POST)
        formset = ProductUnitFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            product = form.save()
            formset.instance = product
            formset.save()
            return redirect('stock:product_list')
    else:
        form = ProductForm()
        formset = ProductUnitFormSet()
    return render(request, 'stock/product_form.html', {'form': form, 'formset': formset})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    ProductUnitFormSet = inlineformset_factory(Product, ProductUnit, form=ProductUnitForm, extra=0, can_delete=True)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        formset = ProductUnitFormSet(request.POST, instance=product)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('stock:product_list')
    else:
        form = ProductForm(instance=product)
        formset = ProductUnitFormSet(instance=product)
    return render(request, 'stock/product_form.html', {'form': form, 'formset': formset})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect('stock:product_list')
    return render(request, 'stock/product_confirm_delete.html', {'product': product})

# --- Unit Views (for managing individual units) ---

def unit_list(request):
    units = Unit.objects.all()
    return render(request, 'stock/unit_list.html', {'units': units})

def unit_create(request):
    if request.method == "POST":
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stock:unit_list')
    else:
        form = UnitForm()
    return render(request, 'stock/unit_form.html', {'form': form})

def unit_update(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    if request.method == "POST":
        form = UnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            return redirect('stock:unit_list')
    else:
        form = UnitForm(instance=unit)
    return render(request, 'stock/unit_form.html', {'form': form})

def unit_delete(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    if request.method == "POST":
        unit.delete()
        return redirect('stock:unit_list')
    return render(request, 'stock/unit_confirm_delete.html', {'unit': unit})
