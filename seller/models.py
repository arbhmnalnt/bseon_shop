from django.db import models
from stock.models import Product, ProductUnit

class Invoice(models.Model):
    customer_name = models.CharField(max_length=255, verbose_name="اسم العميل")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="الإجمالى")
    created_at = models.DateTimeField(auto_now_add=True)
    canceled = models.BooleanField(default=False)

    def __str__(self):
        return f"Invoice #{self.id}"

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_unit = models.ForeignKey(ProductUnit, on_delete=models.CASCADE, verbose_name="الوحدة")
    quantity = models.PositiveIntegerField(default=1)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False, verbose_name="الإجمالى")

    def save(self, *args, **kwargs):
        # Set the price based on the selected product unit
        self.price_per_unit = self.product_unit.sell_price
        self.total_price = self.quantity * self.price_per_unit
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} ({self.product_unit.unit.name}) - {self.invoice}"
