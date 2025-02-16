# Generated by Django 4.2 on 2025-02-16 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('base_unit', models.CharField(default='piece', help_text='Smallest unit (e.g., gram, bottle, piece)', max_length=50)),
                ('big_unit', models.CharField(blank=True, help_text='Larger unit (e.g., carton, dozen). Leave blank if not applicable.', max_length=50, null=True)),
                ('units_in_big_unit', models.PositiveIntegerField(blank=True, help_text='Number of base units in one big unit (e.g., 12 for a dozen)', null=True)),
                ('buy_price_big', models.DecimalField(blank=True, decimal_places=2, help_text='Purchase price per big unit (if applicable)', max_digits=10, null=True)),
                ('sell_price_base', models.DecimalField(decimal_places=2, help_text='Selling price per base unit', max_digits=10)),
                ('category', models.CharField(blank=True, max_length=100, null=True)),
                ('supplier', models.CharField(blank=True, max_length=100, null=True)),
                ('stock_quantity', models.PositiveIntegerField(default=0)),
                ('barcode', models.CharField(blank=True, max_length=50, null=True, unique=True)),
            ],
        ),
    ]
