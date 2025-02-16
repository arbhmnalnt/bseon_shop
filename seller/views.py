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
        return JsonResponse({'price': float(product.price)})
    except Product.DoesNotExist:
        return JsonResponse({'price': 0})

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