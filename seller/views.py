from django.shortcuts import render, redirect
from django.forms import formset_factory
from .models import Invoice, InvoiceItem
from .forms import InvoiceForm, InvoiceItemForm
from django.forms import inlineformset_factory
from django.http import JsonResponse
from stock.models import Product
from django.shortcuts import get_object_or_404

def invoice_detail(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    return render(request, 'seller/invoice_detail.html', {'invoice': invoice})

def invoice_list(request):
    invoices = Invoice.objects.all().order_by('-created_at')  # Show latest first
    return render(request, 'seller/invoice_list.html', {'invoices': invoices})
def get_product_price(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        data = {
            "sell_price_base": float(product.sell_price_base),
            "big_unit": product.big_unit if product.big_unit else "",
            "units_in_big_unit": product.units_in_big_unit if product.units_in_big_unit else 1,
            "base_unit": product.base_unit,
        }
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({"sell_price_base": 0, "big_unit": "", "units_in_big_unit": 1, "base_unit": ""})

def create_invoice(request):
    InvoiceItemFormSet = inlineformset_factory(
        Invoice, InvoiceItem, form=InvoiceItemForm, extra=2, can_delete=True
    )
    if request.method == 'POST':
        invoice_form = InvoiceForm(request.POST)
        formset = InvoiceItemFormSet(request.POST, prefix='items')
        if invoice_form.is_valid() and formset.is_valid():
            invoice = invoice_form.save()
            total_price = 0
            for item in formset.save(commit=False):
                item.invoice = invoice
                # Calculate each invoice item's total price
                item.total_price = item.quantity * item.price_per_unit
                item.save()
                total_price += item.total_price
            invoice.total_price = total_price
            invoice.save()
            return redirect('seller:invoice-list')
    else:
        invoice_form = InvoiceForm()
        formset = InvoiceItemFormSet(prefix='items')

    return render(request, 'seller/create_invoice.html', {
        'invoice_form': invoice_form,
        'formset': formset,
    })