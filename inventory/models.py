from django.db import models

# 🟩 وحدة القياس (قطعة - كرتونة - كيلو ...)
class Unit(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name="اسم الوحدة")

    def __str__(self):
        return self.name

# 🟩 المنتج الرئيسي
class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="اسم المنتج")
    category = models.CharField(max_length=255, null=True, blank=True, verbose_name="التصنيف")
    description = models.TextField(blank=True, null=True, verbose_name="الوصف")

    def __str__(self):
        return self.name

# 🟩 الوحدات المرتبطة بكل منتج (مع الكمية والسعر)
class ProductUnit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='units', verbose_name="المنتج")
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, verbose_name="الوحدة")
    level = models.PositiveIntegerField(verbose_name="المستوى (1 للأكبر)")
    conversion_factor = models.DecimalField(max_digits=10, decimal_places=2, default=1, verbose_name="عدد الوحدات الأقل")
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="سعر التكلفة")
    sell_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="سعر البيع")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="الكمية المتاحة")

    class Meta:
        unique_together = ('product', 'unit')
        ordering = ['level']

    def __str__(self):
        return f"{self.product.name} - {self.unit.name} ({self.quantity})"
