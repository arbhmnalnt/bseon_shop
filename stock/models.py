from django.db import models

class Unit(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    # Optionally, set a base unit (e.g., the largest unit)
    base_unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True, related_name='base_unit_products')
    supplier = models.CharField(max_length=255, blank=True, null=True, default='افتراضى', verbose_name="المورد")
    kind = models.CharField(max_length=255, blank=True, null=True, default='افتراضى', verbose_name="التصنيف")
    def __str__(self):
        return self.name

class ProductUnit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='units')
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True)
    level = models.PositiveIntegerField(help_text="Hierarchy level (1 for the largest, then 2, etc.)")
    conversion_factor = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=1, 
        help_text="Number of lower-level units per one unit of this level"
    )
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sell_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ('product', 'level')
        ordering = ['level']

    def __str__(self):
        return f"{self.product.name} - {self.unit.name} (Level {self.level})"
