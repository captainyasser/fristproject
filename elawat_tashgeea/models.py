# elawat_tashgeea/models.py
from django.db import models
from em_data.models import Employee  # تأكد من المسار الصحيح للموديل Employee
from django.utils import timezone

class ElawaRecord(models.Model):
    """
    سجل علاوة تشجيعية لموظف واحد.
    كل إدخال يمثل (رقم القرار - تاريخ العلاوة - ملاحظات) مربوط بموظف.
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='elawat')
    decision_number = models.CharField(max_length=100, null=True, blank=True, verbose_name="رقم القرار")
    elawa_date = models.DateField(verbose_name="تاريخ العلاوة")
    notes = models.TextField(null=True, blank=True, verbose_name="ملاحظات")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'elawat_tashgeea_records'
        ordering = ['-elawa_date', '-created_at']
        verbose_name = "سجل علاوة تشجيعية"
        verbose_name_plural = "سجلات العلاوات التشجيعية"

    def __str__(self):
        return f"{self.employee.name} - {self.decision_number} ({self.elawa_date})"

class NominationRecord(models.Model):
    """
    سجل ترشيح موظف لعلاوة تشجيعية في سنة معينة.
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='nominations')
    year = models.IntegerField(verbose_name="عام الترشيح")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'elawat_tashgeea_nominations'
        unique_together = ('employee', 'year')
        verbose_name = "ترشيح علاوة تشجيعية"
        verbose_name_plural = "ترشيحات العلاوة التشجيعية"

    def __str__(self):
        return f"{self.employee.name} - مرشح لعام {self.year}"
