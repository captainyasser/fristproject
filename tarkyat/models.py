from django.db import models
from em_data.models import Employee
from ranks.models import Rank

class Promotion(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='promotions', verbose_name="الموظف")
    from_rank = models.ForeignKey(Rank, on_delete=models.SET_NULL, null=True, blank=True, related_name='promotions_from', verbose_name="الدرجة السابقة")
    to_rank = models.ForeignKey(Rank, on_delete=models.CASCADE, related_name='promotions_to', verbose_name="الدرجة الجديدة")
    promotion_date = models.DateField(verbose_name="تاريخ الترقية")
    promotion_course_number = models.CharField(max_length=50, verbose_name="رقم دورة الترقية")
    training_start_date = models.DateField(verbose_name="تاريخ بداية الدورة")
    training_end_date = models.DateField(verbose_name="تاريخ نهاية الدورة")
    training_course_number = models.CharField(max_length=50, verbose_name="رقم الدورة التأهيلية")
    training_location = models.CharField(max_length=255, verbose_name="مكان انعقاد الدورة")
    notes = models.TextField(null=True, blank=True, verbose_name="ملاحظات")

    class Meta:
        verbose_name = "ترقية"
        verbose_name_plural = "الترقيات"
        ordering = ["-promotion_date"]

    def __str__(self):
        return f"{self.employee.name} من {self.from_rank} إلى {self.to_rank} - {self.promotion_date}"