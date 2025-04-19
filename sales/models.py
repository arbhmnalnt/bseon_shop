# sales/models.py

from django.db import models
from inventory.models import ProductUnit

class Sale(models.Model):
    STATUS_CHOICES = (
        ('draft', 'مسودة'),
        ('final', 'نهائية'),
    )

    customer_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="اسم العميل"
    )
    date = models.DateField(
        auto_now_add=True,
        verbose_name="تاريخ البيع"
    )
    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="الإجمالي"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='final',
        verbose_name="الحالة"
    )

    class Meta:
        verbose_name = "فاتورة بيع"
        verbose_name_plural = "فواتير البيع"
        ordering = ['-date']

    def __str__(self):
        return f"فاتورة بيع #{self.id} - {self.customer_name or 'عميل عام'}"


class SaleItem(models.Model):
    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="فاتورة البيع"
    )
    product_unit = models.ForeignKey(
        ProductUnit,
        on_delete=models.PROTECT,
        verbose_name="وحدة المنتج"
    )
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="الكمية"
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="سعر الوحدة"
    )
    line_total = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        editable=False,
        verbose_name="المجموع"
    )

    class Meta:
        verbose_name = "بند بيع"
        verbose_name_plural = "بنود البيع"

    def save(self, *args, **kwargs):
        # حساب المجموع قبل الحفظ
        self.line_total = self.quantity * self.price
        super().save(*args, **kwargs)
        # خصم الكمية من المخزون
        pu = self.product_unit
        pu.quantity -= self.quantity
        pu.save()

    def __str__(self):
        return f"{self.product_unit.product.name} - {self.quantity} {self.product_unit.unit.name}"
