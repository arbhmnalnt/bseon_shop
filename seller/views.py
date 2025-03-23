from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import *
from stock.models import ProductUnit
from django.http import JsonResponse


def invoice_list(request):
    invoices = Invoice.objects.all().order_by('-created_at')
    return render(request, 'seller/invoice_list.html', {'invoices': invoices})

def invoice_create(request):
    InvoiceItemFormSet = inlineformset_factory(Invoice, InvoiceItem, form=InvoiceItemForm, extra=1, can_delete=True)
    if request.method == "POST":
        form = InvoiceForm(request.POST)
        formset = InvoiceItemFormSet(request.POST)
        # Update product_unit queryset for each form based on selected product
        for f in formset:
            product_id = f.data.get(f.add_prefix('product'))
            if product_id:
                f.fields['product_unit'].queryset = ProductUnit.objects.filter(product_id=product_id)
            else:
                f.fields['product_unit'].queryset = ProductUnit.objects.none()

        if form.is_valid() and formset.is_valid():
            print("Total forms submitted:", len(formset.cleaned_data))
            invoice = form.save()  # Create the invoice
            formset.instance = invoice
            formset.save()         # Save invoice items
            
            # Calculate the total for the invoice
            total = 0
            for item in invoice.items.all():
                line_total = item.quantity * item.price_per_unit
                print(f"Item: {item.product.name}, Quantity: {item.quantity}, Price: {item.price_per_unit}, Line Total: {line_total}")
                total += line_total
            invoice.total_price = total
            print("Calculated Total:", total)
            
            invoice.total_price = total
            invoice.save()
            return redirect('seller:invoice_list')
        else:
            print("Form Errors:", form.errors)
            print("Formset Errors:", formset.errors)
    else:
        form = InvoiceForm()
        formset = InvoiceItemFormSet()
    return render(request, 'seller/invoice_form.html', {'form': form, 'formset': formset})


def invoice_update(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    # Create the inline formset class with extra=0
    InvoiceItemFormSet = inlineformset_factory(
        Invoice,
        InvoiceItem,
        form=InvoiceItemForm,
        extra=0,
        can_delete=True
    )
    
    if request.method == "POST":
        form = InvoiceForm(request.POST, instance=invoice)
        formset = InvoiceItemFormSet(request.POST, instance=invoice, prefix="items")
        
        # Debug prints for management form and POST data.
        print("Management form data:", formset.management_form.data)
        print("POST Data:", request.POST)
        
        # Update product_unit queryset for each form in the formset.
        for f in formset:
            product_id = f.data.get(f.add_prefix('product'))
            if product_id:
                qs = ProductUnit.objects.filter(product_id=product_id)
                if f.instance.pk and f.instance.product_unit:
                    qs = qs | ProductUnit.objects.filter(pk=f.instance.product_unit.pk)
                f.fields['product_unit'].queryset = qs.distinct()
            else:
                f.fields['product_unit'].queryset = ProductUnit.objects.none()
        
        if form.is_valid() and formset.is_valid():
            form.save()  # Save the main invoice.
            formset.save()  # Save invoice items.
            
            # Recalculate invoice total.
            total = 0
            for item in invoice.items.all():
                line_total = item.quantity * item.price_per_unit
                print(f"Item: {item.product.name}, Quantity: {item.quantity}, Price: {item.price_per_unit}, Line Total: {line_total}")
                total += line_total
            invoice.total_price = total
            invoice.save()
            print("Invoice updated successfully. Total:", total)
            return redirect('seller:invoice_list')
        else:
            print("Update Form Errors:", form.errors)
            print("Update Formset Errors:", formset.errors)
    else:
        form = InvoiceForm(instance=invoice)
        formset = InvoiceItemFormSet(instance=invoice, prefix="items")
    
    return render(request, 'seller/invoice_form.html', {'form': form, 'formset': formset})


def invoice_delete(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == "POST":
        invoice.delete()
        return redirect('seller:invoice_list')
    return render(request, 'seller/invoice_confirm_delete.html', {'invoice': invoice})

def invoice_detail(request, pk):
    """
    Display detailed information for a specific invoice.
    """
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, 'seller/invoice_detail.html', {'invoice': invoice})

def get_product_price(request):
    """
    Given a product and product_unit, return its sell price.
    Expects GET parameters: product_id and product_unit_id.
    """
    product_id = request.GET.get('product_id')
    product_unit_id = request.GET.get('product_unit_id')
    try:
        # Ensure the unit is part of the selected product
        product_unit = ProductUnit.objects.get(id=product_unit_id, product_id=product_id)
        price = product_unit.sell_price
        return JsonResponse({'price': float(price)})
    except ProductUnit.DoesNotExist:
        return JsonResponse({'price': 0})

def get_product_units(request):
    product_id = request.GET.get('product_id')
    units = ProductUnit.objects.filter(product_id=product_id).values('id', 'unit__name', 'conversion_factor', 'cost_price', 'sell_price')
    return JsonResponse({'units': list(units)})