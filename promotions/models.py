from django.db import models
from em_data.models import Employee  # استيراد نموذج الموظف
from ranks.models import Rank  # استيراد نموذج الدرجات

class Promotion(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="الموظف")
    from_rank = models.ForeignKey(Rank, related_name="from_promotions", on_delete=models.CASCADE, verbose_name="من درجة")
    to_rank = models.ForeignKey(Rank, related_name="to_promotions", on_delete=models.CASCADE, verbose_name="إلى درجة")
    promotion_date = models.DateField(verbose_name="تاريخ الترقية")
    course_number = models.CharField(max_length=50, verbose_name="رقم الدورة", blank=True, null=True)
    promotion_type = models.CharField(
        max_length=20,
        choices=[("عادية", "عادية"), ("استثنائية", "استثنائية")],
        default="عادية",
        verbose_name="نوع الترقية"
    )
    course_start_date = models.DateField(verbose_name="تاريخ بدء الفرقة", blank=True, null=True)
    course_end_date = models.DateField(verbose_name="تاريخ انتهاء الفرقة", blank=True, null=True)
    training_institution = models.CharField(max_length=255, verbose_name="الجهة التدريبية", blank=True, null=True)
    result = models.CharField(
        max_length=20,
        choices=[("ناجح", "ناجح"), ("راسب", "راسب"), ("إلغاء", "إلغاء")],
        verbose_name="النتيجة",
        blank=True,
        null=True
    )
    notes = models.TextField(verbose_name="ملاحظات", blank=True, null=True)

    def __str__(self):
        return f"{self.employee} - {self.from_rank} إلى {self.to_rank}"

    class Meta:
        verbose_name = "ترقية"
        verbose_name_plural = "الترقيات"
        ordering = ["-promotion_date"]  # ترتيب الترقيات من الأحدث إلى الأقدم
