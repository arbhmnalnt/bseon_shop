from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, blank=True, null=True)
    supplier = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    barcode = models.CharField(max_length=50, blank=True, null=True, unique=True)

    def __str__(self):
        return self.name
