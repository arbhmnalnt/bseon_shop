from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Product
from .forms import ProductForm

# List all products
class ProductListView(ListView):
    model = Product
    template_name = 'stock/product_list.html'
    context_object_name = 'products'

# Create a new product
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'stock/product_form.html'
    success_url = reverse_lazy('stock:product-list')

# Update an existing product
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'stock/product_form.html'
    success_url = reverse_lazy('stock:product-list')

# Delete a product
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'stock/product_confirm_delete.html'
    success_url = reverse_lazy('product-list')
