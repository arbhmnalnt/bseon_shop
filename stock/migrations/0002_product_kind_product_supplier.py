# Generated by Django 5.1.7 on 2025-03-20 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='kind',
            field=models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='التصنيف'),
        ),
        migrations.AddField(
            model_name='product',
            name='supplier',
            field=models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='المورد'),
        ),
    ]
