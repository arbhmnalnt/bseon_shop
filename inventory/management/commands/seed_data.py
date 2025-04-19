import random
from datetime import timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone

from suppliers.models import Supplier
from inventory.models import Unit, Product, ProductUnit
from purchases.models import Purchase, PurchaseItem
from sales.models import Sale, SaleItem

class Command(BaseCommand):
    help = "Wipe & seed the DB with dummy suppliers, products, purchases, and sales."

    def handle(self, *args, **options):
        self.stdout.write("🔄 Clearing existing data…")
        # delete children first
        SaleItem.objects.all().delete()
        Sale.objects.all().delete()
        PurchaseItem.objects.all().delete()
        Purchase.objects.all().delete()
        ProductUnit.objects.all().delete()
        Product.objects.all().delete()
        Unit.objects.all().delete()
        Supplier.objects.all().delete()

        # 1) Suppliers
        self.stdout.write("✅ Creating suppliers…")
        supplier_names = ["مورد الفواكه", "مورد الألبان", "مورد البقالة"]
        suppliers = [Supplier.objects.create(name=n) for n in supplier_names]
        self.stdout.write(f"  • {len(suppliers)} suppliers")

        # 2) Units
        self.stdout.write("✅ Creating units…")
        unit_names = ["قطعة", "كيلو", "علبة"]
        units = [Unit.objects.create(name=n) for n in unit_names]
        self.stdout.write(f"  • {len(units)} units")

        # 3) Products + ProductUnits
        self.stdout.write("✅ Creating products + units…")
        product_names = ["بيض أبيض", "مكرونة", "حليب"]
        products = []
        for pname in product_names:
            p = Product.objects.create(
                name=pname,
                category="بقالة",
                description=f"هذا وصف {pname}"
            )
            products.append(p)
            # attach each unit type with random prices
            for u in units:
                ProductUnit.objects.create(
                    product=p,
                    unit=u,
                    level=random.randint(1, 3),
                    conversion_factor=1,
                    cost_price=Decimal(random.uniform(5, 20)).quantize(Decimal("0.01")),
                    sell_price=Decimal(random.uniform(10, 30)).quantize(Decimal("0.01")),
                    quantity=0
                )
        self.stdout.write(f"  • {len(products)} products and {len(products)*len(units)} product-units")

        # 4) Purchases
        self.stdout.write("✅ Seeding purchases…")
        today = timezone.localdate()
        for supplier in suppliers:
            for _ in range(2):  # 2 purchases per supplier
                date = today - timedelta(days=random.randint(5, 30))
                pur = Purchase.objects.create(
                    supplier=supplier,
                    date=date,
                    notes="بيانات اختبارية"
                )
                total = Decimal("0.00")
                # pick 3 random product-units
                pus = list(ProductUnit.objects.order_by('?')[:3])
                for pu in pus:
                    qty = random.randint(5, 30)
                    price = pu.cost_price
                    line_total = price * qty
                    PurchaseItem.objects.create(
                        purchase=pur,
                        product_unit=pu,
                        quantity=qty,
                        price=price
                    )
                    total += line_total
                    # update stock
                    pu.quantity += qty
                    pu.save(update_fields=["quantity"])
                # save total
                pur.total = total
                pur.save(update_fields=["total"])
        self.stdout.write("  • Purchases seeded")

        # 5) Sales
        self.stdout.write("✅ Seeding sales…")
        for i in range(5):
            sale = Sale.objects.create(
                customer_name=f"عميل{i+1}",
                status="final"
                # date will default to auto_now_add or your default
            )
            total = Decimal("0.00")
            # pick 3 random in‑stock product-units
            available = ProductUnit.objects.filter(quantity__gt=0).order_by('?')[:3]
            for pu in available:
                max_qty = min(pu.quantity, 5)
                qty = random.randint(1, max_qty)
                price = pu.sell_price
                line_total = price * qty
                SaleItem.objects.create(
                    sale=sale,
                    product_unit=pu,
                    quantity=qty,
                    price=price
                )
                total += line_total
                # decrement stock
                pu.quantity -= qty
                pu.save(update_fields=["quantity"])
            sale.total = total
            sale.save(update_fields=["total"])
        self.stdout.write("  • Sales seeded")

        self.stdout.write(self.style.SUCCESS("🎉 Done! Database reset and dummy data loaded."))
