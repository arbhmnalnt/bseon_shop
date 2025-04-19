from django.db import models
from suppliers.models import Supplier
from inventory.models import ProductUnit
from django.utils import timezone

class Purchase(models.Model):
    supplier   = models.ForeignKey(Supplier, on_delete=models.PROTECT, verbose_name="المورد")
    date       = models.DateField(default=timezone.localdate, verbose_name="تاريخ الشراء")
    total      = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="الإجمالي")
    notes      = models.TextField(blank=True, null=True, verbose_name="ملاحظات")

    def __str__(self):
        return f"فاتورة شراء #{self.id} - {self.supplier.name}"

class PurchaseItem(models.Model):
    purchase   = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='items', verbose_name="فاتورة الشراء")
    product_unit = models.ForeignKey(ProductUnit, on_delete=models.PROTECT, verbose_name="وحدة المنتج")
    quantity   = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="الكمية")
    price      = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="سعر الوحدة")
    line_total = models.DecimalField(max_digits=14, decimal_places=2, editable=False, verbose_name="المجموع")

    class Meta:
        verbose_name = "بند شراء"
        verbose_name_plural = "بنود الشراء"

    def save(self, *args, **kwargs):
        # حساب مجموع السطر قبل الحفظ
        self.line_total = self.quantity * self.price
        super().save(*args, **kwargs)
        # بعد الحفظ، تحديث المخزون
        pu = self.product_unit
        pu.quantity += self.quantity
        pu.save()

    def __str__(self):
        return f"{self.product_unit.product.name} - {self.quantity} {self.product_unit.unit.name}"
