from django.db import models
from suppliers.models import Supplier   # ← import Supplier

class Unit(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name="اسم الوحدة")
    def __str__(self):
        return self.name

class Product(models.Model):
    name        = models.CharField(max_length=255, verbose_name="اسم المنتج")
    category    = models.CharField(max_length=255, blank=True, null=True, verbose_name="التصنيف")
    description = models.TextField(blank=True, null=True, verbose_name="الوصف")
    supplier    = models.ForeignKey(Supplier, on_delete=models.PROTECT,
                                    verbose_name="المورد", blank=True, null=True)  # ← new field

    def __str__(self):
        return self.name

class ProductUnit(models.Model):
    product           = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='units', verbose_name="المنتج")
    unit              = models.ForeignKey(Unit, on_delete=models.CASCADE, verbose_name="الوحدة")
    level             = models.PositiveIntegerField(verbose_name="المستوى (1 للأكبر)")
    conversion_factor = models.DecimalField(max_digits=10, decimal_places=2, default=1, verbose_name="عدد الوحدات الأقل")
    cost_price        = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="سعر التكلفة")

    price_1           = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="السعر 1 (أساسي)")
    price_2           = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="السعر 2 (عرض)")
    price_3           = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="السعر 3 (VIP)")

    quantity          = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="الكمية المتاحة")

    class Meta:
        unique_together = ('product', 'unit')
        ordering = ['level']

    def __str__(self):
        return f"{self.product.name} - {self.unit.name} ({self.quantity})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # لو دي الوحدة الأكبر (مستوى 1) — حدّث باقي الوحدات
        if self.level == 1:
            siblings = ProductUnit.objects.filter(product=self.product).exclude(id=self.id)
            for sibling in siblings:
                if sibling.conversion_factor > 0:
                    sibling.price_1 = round(self.price_1 / sibling.conversion_factor, 2)
                    sibling.price_2 = round(self.price_2 / sibling.conversion_factor, 2)
                    sibling.price_3 = round(self.price_3 / sibling.conversion_factor, 2)
                    sibling.save()