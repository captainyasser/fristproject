from django.db import models
from em_data.models import Employee
from ranks.models import Rank

class Promotion(models.Model):
    PROMOTION_TYPES = [
        ('normal', 'عادية'),
        ('exceptional', 'استثنائية'),
        ('cadre', 'كادر أمناء'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='promotions', verbose_name="الموظف")
    from_rank = models.ForeignKey(Rank, on_delete=models.SET_NULL, null=True, blank=True, related_name='promotions_from', verbose_name="الدرجة السابقة")
    to_rank = models.ForeignKey(Rank, on_delete=models.CASCADE, related_name='promotions_to', verbose_name="الدرجة الجديدة")
    promotion_date = models.DateField(verbose_name="تاريخ الترقية")
    promotion_course_number = models.CharField(max_length=50, null=True, blank=True, verbose_name="رقم دورة الترقية")
    training_start_date = models.DateField(null=True, blank=True, verbose_name="تاريخ بداية الدورة")
    training_end_date = models.DateField(null=True, blank=True, verbose_name="تاريخ نهاية الدورة")
    training_course_number = models.CharField(null=True, blank=True, max_length=50, verbose_name="رقم الدورة التأهيلية")
    training_location = models.CharField(null=True, blank=True, max_length=255, verbose_name="مكان انعقاد الدورة")
    notes = models.TextField(null=True, blank=True, verbose_name="ملاحظات")
    promotion_type = models.CharField(
        max_length=20,
        choices=PROMOTION_TYPES,
        null=True,
        blank=True,
        verbose_name="نوع الترقية"
    )

    class Meta:
        verbose_name = "ترقية"
        verbose_name_plural = "الترقيات"
        ordering = ["-promotion_date"]

    def __str__(self):
        promotion_type_display = self.get_promotion_type_display() if self.promotion_type else "غير محدد"
        return f"{self.employee.name} من {self.from_rank} إلى {self.to_rank} - {self.promotion_date} ({promotion_type_display})"
