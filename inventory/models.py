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
    sell_price        = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="سعر البيع")
    quantity          = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="الكمية المتاحة")

    class Meta:
        unique_together = ('product', 'unit')
        ordering = ['level']


    def __str__(self):
        return str(self.product.name)

    def save(self, *args, **kwargs):
        # 1) Save this unit’s own cost & sell price first
        super().save(*args, **kwargs)

        # 2) Find all "higher" units (bigger packaging) for the same product
        siblings = ProductUnit.objects.\
            filter(product=self.product, level__lt=self.level).\
            order_by('-level')

        # 3) Propagate this unit's costs up the chain
        #    For each sibling unit at a smaller level (bigger package),
        #    multiply by its conversion_factor to get its cost & sell prices
        for sibling in siblings:
            sibling.cost_price = sibling.conversion_factor * self.cost_price
            sibling.sell_price = sibling.conversion_factor * self.sell_price
            super(ProductUnit, sibling).save(update_fields=['cost_price','sell_price'])