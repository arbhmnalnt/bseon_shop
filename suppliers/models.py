from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=255, verbose_name="اسم المورد", blank=True, null=True)
    phone = models.CharField(max_length=20, verbose_name="رقم الهاتف", blank=True, null=True)
    email = models.EmailField(verbose_name="البريد الإلكتروني", blank=True, null=True)
    address = models.TextField(verbose_name="العنوان", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخر تحديث")

    def __str__(self):
        return self.name
