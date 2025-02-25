from django.db import models

class Unit(models.Model):
    name = models.CharField(max_length=20, unique=True)  # Store unit names dynamically

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, blank=True, null=True)
    supplier = models.CharField(max_length=100, blank=True, null=True)
    
    # Pricing based on unit type
    big_unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True, related_name='big_unit_products')
    big_unit_cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    big_unit_sell_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    small_unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True, related_name='small_unit_products')
    small_units_counts = models.PositiveIntegerField(default=1)  # Default is 1 if no small unit
    small_unit_cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    small_unit_sell_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    stock_quantity_big = models.PositiveIntegerField(default=0)  # Stock in big units
    barcode = models.CharField(max_length=50, blank=True, null=True, unique=True)

    def __str__(self):
        return f'{self.name} [ {self.big_unit.name if self.big_unit else "No Unit"}]'

    def get_total_stock_small_units(self):
        """Converts big unit stock to small unit count if applicable"""
        if self.small_unit and self.small_units_counts:
            return self.stock_quantity_big * self.small_units_counts
        return self.stock_quantity_big  # If no small unit, return as is

class StockEntry(models.Model):
    """Handles stock entries for purchases or stock adjustments"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)  # Either big or small unit
    quantity = models.PositiveIntegerField()
    transaction_type = models.CharField(max_length=10, choices=[('IN', 'Stock In'), ('OUT', 'Stock Out')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name} [ {self.product.big_unit.name if self.product.big_unit else "No Unit"}]'

    def save(self, *args, **kwargs):
        """Automatically updates product stock when saved"""
        super().save(*args, **kwargs)
        if self.unit == self.product.big_unit:
            if self.transaction_type == 'IN':
                self.product.stock_quantity_big += self.quantity
            elif self.transaction_type == 'OUT':
                self.product.stock_quantity_big -= self.quantity
        elif self.unit == self.product.small_unit and self.product.small_units_counts:
            if self.transaction_type == 'IN':
                self.product.stock_quantity_big += self.quantity / self.product.small_units_counts
            elif self.transaction_type == 'OUT':
                self.product.stock_quantity_big -= self.quantity / self.product.small_units_counts        
        self.product.save()
