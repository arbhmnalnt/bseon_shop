# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, StockEntry
from .forms import ProductForm, StockEntryForm

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stock:product_list')
    else:
        form = ProductForm()
    return render(request, 'stock/product_form.html', {'form': form})
                  
def product_delete(request):
    pass

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('stock/product_list.html')
    else:
        form = ProductForm(instance=product)
    return render(request, 'stock/product_form.html', {'form': form})
def product_list(request):
    products = Product.objects.all()
    ctx = {'products': products}
    return render(request, 'stock/product_list.html', ctx)