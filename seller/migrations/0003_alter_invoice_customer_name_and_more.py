# Generated by Django 5.1.6 on 2025-02-24 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0002_remove_invoice_updated_at_invoice_canceled_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='customer_name',
            field=models.CharField(max_length=255, verbose_name='اسم العميل'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='الإجمالى'),
        ),
        migrations.AlterField(
            model_name='invoiceitem',
            name='total_price',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=10, verbose_name='الإجمالى'),
        ),
    ]
