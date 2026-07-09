from django.db import models
from django.core.validators import RegexValidator


class Quote(models.Model):
    PRODUCT_CHOICES = [
        ("ksara", "كسارة"),
        ("mixer", "ميكسر"),
        ("makbs", "مكبس"),
        ("hala", "حلة استاندرد"),
        ("table1", "ترابيزة"),
        ("troly1", "ترولي لانشون"),
        ("troly2", "ترولي صاجات"),
        ("qalep", "قالب لانشون"),
    ]

    STATUS_CHOICES = [
        ("new", "جديد"),
        ("contacted", "تم التواصل"),
        ("quoted", "تم عرض السعر"),
        ("accepted", "تم القبول"),
        ("rejected", "تم الرفض"),
    ]

    product_slug = models.CharField(
        max_length=50,
        choices=PRODUCT_CHOICES,
        verbose_name="نوع المنتج"
    )
    name = models.CharField(max_length=100, verbose_name="الاسم")
    phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(r'^01\d{9}$', 'رقم موبايل مصري غير صحيح')],
        verbose_name="الموبايل"
    )
    email = models.EmailField(blank=True, null=True, verbose_name="الإيميل")
    company = models.CharField(max_length=100, blank=True, null=True, verbose_name="الشركة")
    message = models.TextField(verbose_name="الطلب")

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new",
        verbose_name="الحالة"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "طلب عرض سعر"
        verbose_name_plural = "طلبات عروض الأسعار"

    def __str__(self):
        return f"{self.name} - {self.get_product_slug_display()} ({self.phone})"