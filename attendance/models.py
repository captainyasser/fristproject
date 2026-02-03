from django.db import models
from em_data.models import Employee

class Attendance(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='attendances',
        verbose_name="الفرد"
    ) 
    date = models.DateField(verbose_name="التاريخ")
    state = models.CharField(
        max_length=20,
        choices=[
            ('_', '-'),
            ('نوبتجي', 'نوبتجي'),
            ('يومي', 'يومي'),
            ('راحة', 'راحة'),
            ('دورية', 'دورية'),
            ('ر بديلة', 'ر بديلة'),
            ('طارئة', 'طارئة'),
            ('مأمورية', 'مأمورية'),
            ('مأمورية خ', 'مأمورية خ'),
            ('فرقة', 'فرقة'),
            ('انتداب', 'انتداب'),
            ('مرضي', 'مرضي'),
            ('ج وضع', 'ج وضع'),
            ('خاصه', 'خاصه'),
            ('8 صباحاً', '8 صباحاً'),
            ('ت دوري', 'ت دوري'),
            ('ت تكراري', 'ت تكراري'),
            ('منحة', 'منحة'),
            ('عطلة', 'عطلة'),
            ('غياب', 'غياب'),
            ('قرار66', 'قرار66'),
        ],
        default='_',
        verbose_name="حالة الحضور"
    )
    food = models.BooleanField(default=False, verbose_name="تعيين طعام")
    comfort_adjustment = models.IntegerField(
        default=0,
        choices=[(0, 'لا تغيير'), (1, '+1'), (-1, '-1')],
        verbose_name="تعديل رصيد الراحة"
    )
    
    in_or_out = models.CharField(max_length=10, choices=[('in', 'In'), ('going', 'Going'), ('out', 'Out')], default='') 
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "حضور"
        verbose_name_plural = "سجل الحضور"
        unique_together = ('employee', 'date')

    def __str__(self):
        return f"{self.employee.name} - {self.date} - {self.state}"


from django.conf import settings

class AttendanceChangeLog(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, related_name='change_logs')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Snapshot of values BEFORE the change
    prev_state = models.CharField(max_length=20)
    prev_food = models.BooleanField()
    prev_comfort_adjustment = models.IntegerField()
    prev_in_or_out = models.CharField(max_length=10)
    
    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Log: {self.attendance} at {self.timestamp}"


class AttendanceRedoLog(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, related_name='redo_logs')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Snapshot of values that we UNDID (so we can REDO to them)
    redo_state = models.CharField(max_length=20)
    redo_food = models.BooleanField()
    redo_comfort_adjustment = models.IntegerField()
    redo_in_or_out = models.CharField(max_length=10)
    
    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Redo Log: {self.attendance} at {self.timestamp}"
