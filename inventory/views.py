from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm, ProductUnitForm

def add_product_unit(request, product_id=None):
    if request.method == 'POST':
        form = ProductUnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=form.cleaned_data['product'].id)
    else:
        form = ProductUnitForm(initial={'product': product_id} if product_id else None)
    return render(request, 'inventory/add_product_unit.html', {'form': form})
# 🟢 عرض قائمة المنتجات
def product_list(request):
    products = Product.objects.all()
    return render(request, 'inventory/product_list.html', {'products': products})

# 🟢 عرض تفاصيل منتج
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'inventory/product_detail.html', {'product': product})

# 🟢 إنشاء منتج جديد
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            new_product = form.save()
            # بعد حفظ المنتج، الانتقال لإضافة وحدة لهذا المنتج مباشرةً
            return redirect('add_product_unit_for_product', product_id=new_product.id)
    else:
        form = ProductForm()

    return render(request, 'inventory/product_form.html', {'form': form})
# 🟢 إضافة وحدة جديدة مرتبطة بمنتج
def add_product_unit(request):
    if request.method == 'POST':
        form = ProductUnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_product_unit')
    else:
        form = ProductUnitForm()
    return render(request, 'inventory/add_product_unit.html', {'form': form})
