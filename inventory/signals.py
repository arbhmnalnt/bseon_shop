from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from purchases.models import PurchaseItem
from sales.models    import SaleItem
from .models         import ProductUnit

# --- PURCHASE ITEMS ---

@receiver(pre_save, sender=PurchaseItem)
def cache_previous_purchase_qty(sender, instance, **kwargs):
    if instance.pk:
        instance._old_qty = PurchaseItem.objects.get(pk=instance.pk).quantity
    else:
        instance._old_qty = 0

@receiver(post_save, sender=PurchaseItem)
def update_stock_on_purchase(sender, instance, created, **kwargs):
    delta = instance.quantity - instance._old_qty
    pu = instance.product_unit
    pu.quantity += delta
    pu.save()

@receiver(post_delete, sender=PurchaseItem)
def revert_stock_on_purchase_delete(sender, instance, **kwargs):
    pu = instance.product_unit
    pu.quantity -= instance.quantity
    pu.save()

# --- SALE ITEMS ---

@receiver(pre_save, sender=SaleItem)
def cache_previous_sale_qty(sender, instance, **kwargs):
    if instance.pk:
        instance._old_qty = SaleItem.objects.get(pk=instance.pk).quantity
    else:
        instance._old_qty = 0

@receiver(post_save, sender=SaleItem)
def update_stock_on_sale(sender, instance, created, **kwargs):
    delta = instance.quantity - instance._old_qty
    pu = instance.product_unit
    pu.quantity -= delta
    pu.save()

@receiver(post_delete, sender=SaleItem)
def revert_stock_on_sale_delete(sender, instance, **kwargs):
    pu = instance.product_unit
    pu.quantity += instance.quantity
    pu.save()
