# Generated by Django 5.2 on 2025-04-20 08:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='saleitem',
            old_name='price',
            new_name='unit_price',
        ),
    ]
