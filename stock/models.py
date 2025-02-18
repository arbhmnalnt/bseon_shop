from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='اسم النمنتج')
    category = models.CharField(max_length=100, blank=True, null=True, verbose_name='التصنسف')
    supplier = models.CharField(max_length=100, blank=True, null=True, verbose_name='المورد')

    # Unit fields:
    base_unit = models.CharField(
        max_length=50,
        default="قطعة واحدة",
        verbose_name='وحدة القياس الاقل'
    )
    big_unit = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="وحدة  القياس الاكبر"
    )
    units_in_big_unit = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='عدد الوحدات الاقل'
    )

    # Pricing
    buy_price_big = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='سعر شراء الوحدة الاكبر - اختيارى'
    )
    sell_price_base = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='سعر بيع الوحدة الاقل'
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
