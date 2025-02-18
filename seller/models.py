from django.db import models
from stock.models import Product

class Invoice(models.Model):
    customer_name = models.CharField(max_length=255)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    canceled = models.BooleanField(default=False)

    def __str__(self):
        return f"Invoice #{self.id}"

class InvoiceItem(models.Model):
    UNIT_CHOICES = (
        ('base', 'الوحدة الاقل'),
        ('big', 'الوحدة الاكبر'),
    )
    invoice = models.ForeignKey(Invoice, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    sold_unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='base', verbose_name='وحدة البيع')
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='سعر الوحدة')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        # Calculate total_price using the entered quantity and price_per_unit
        self.total_price = self.quantity * self.price_per_unit
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} ({self.invoice})"
