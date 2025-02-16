from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, blank=True, null=True)
    supplier = models.CharField(max_length=100, blank=True, null=True)

    # Unit fields:
    base_unit = models.CharField(
        max_length=50,
        default="piece",
        help_text="Smallest unit (e.g., piece, gram, bottle)"
    )
    big_unit = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Larger unit (e.g., carton, dozen). Leave blank if not applicable."
    )
    units_in_big_unit = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Number of base units in one big unit"
    )

    # Pricing
    buy_price_big = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Purchase price per big unit (if applicable)"
    )
    sell_price_base = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Selling price per base unit"
    )

    stock_quantity = models.PositiveIntegerField(default=0)
    barcode = models.CharField(max_length=50, blank=True, null=True, unique=True)

    def __str__(self):
        return self.name

    @property
    def computed_buy_price_base(self):
        """
        If a purchase price for the big unit and a conversion factor are provided,
        return the computed price per base unit.
        """
        if self.buy_price_big and self.units_in_big_unit:
            return self.buy_price_big / self.units_in_big_unit
        return None
