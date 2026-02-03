# E:\yasser\emapi2025\myproject\secret_reports\models.py
from django.db import models
from em_data.models import Employee  # جدول الموظفين الموجود عندك

class SecretReport(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='secret_reports')
    year = models.PositiveIntegerField(verbose_name="السنة")
    score = models.PositiveIntegerField(null=True, blank=True, verbose_name="الدرجة", help_text="من 1 إلى 100")
    notes = models.TextField(null=True, blank=True, verbose_name="ملاحظات")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "secret_reports"
        unique_together = ('employee', 'year')
        ordering = ['-year']

    def __str__(self):
        return f"{self.employee.name} - {self.year} : {self.score}"
