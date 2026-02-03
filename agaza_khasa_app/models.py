# agaza_khasa_app/models.py
from django.db import models
from django.utils import timezone
from em_data.models import Employee

class SpecialLeave(models.Model):
    DURATION_CHOICES = [
        ('يوم', 'يوم'),
        ('شهر', 'شهر'),
        ('سنة', 'سنة'),
    ]

    LEAVE_REASON_CHOICES = [
        ('أجازة وضع', 'أجازة وضع'),
        ('رعاية طفل', 'رعاية طفل'),
        ('رعاية والده', 'رعاية والده'),
        ('رعاية والدته', 'رعاية والدته'),
        ('العمل مدرب موسيقي بدولة الكويت', 'العمل مدرب موسيقي بدولة الكويت'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='special_leaves')
    days_count = models.IntegerField(null=True, blank=True, verbose_name="عدد أيام الإجازة")
    duration_type = models.CharField(max_length=10, choices=DURATION_CHOICES, null=True, blank=True, verbose_name="نوع المدة")
    leave_reason = models.CharField(max_length=100, choices=LEAVE_REASON_CHOICES, verbose_name="سبب الإجازة")
    approval_date = models.DateField(null=True, blank=True, verbose_name="تاريخ الموافقة")
    start_date = models.DateField(null=True, blank=True, verbose_name="تاريخ القيام")
    return_date = models.DateField(null=True, blank=True, verbose_name="تاريخ العودة")
    decision_number = models.CharField(max_length=255, null=True, blank=True, verbose_name="رقم القرار")
    year = models.IntegerField(null=True, blank=True, verbose_name="السنة")
    notes = models.TextField(null=True, blank=True, verbose_name="ملاحظات")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الانشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التعديل")

    class Meta:
        db_table = 'special_leaves'
        ordering = ['-start_date', '-created_at']

    def __str__(self):
        return f"{self.employee.name} - {self.leave_reason} ({self.start_date} => {self.return_date})"
