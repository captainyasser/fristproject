from django.db import models
from departments.models import Department
from ranks.models import Rank
from institutes.models import Institute
from datetime import datetime


class Employee(models.Model):
    # Operation Choices
    OPERATION_CHOICES = [
        ('لم يحدد', 'لم يحدد'),
        ('السبت', 'السبت'),
        ('الأحد', 'الأحد'),
        ('الاثنين', 'الاثنين'),
        ('الثلاثاء', 'الثلاثاء'),
        ('الأربعاء', 'الأربعاء'),
        ('الخميس', 'الخميس'),
        ('الجمعة', 'الجمعة'),
        ('عمل يومي', 'عمل يومي'),
        ('انتداب', 'انتداب'),
        ('قرار66', 'قرار66'),
    ]

    # Marital Status Choices
    MARITAL_STATUS_CHOICES = [
        ('أعزب', 'أعزب'),
        ('متزوج', 'متزوج'),
        ('مطلق', 'مطلق'),
    ]

    # Health Status Choices
    HEALTH_STATUS_CHOICES = [
        ('جيدة', 'جيدة'),
        ('عمل إداري مكتبي', 'عمل إداري مكتبي'),
        ('ممنوع من حمل السلاح', 'ممنوع من حمل السلاح'),
    ]

    id = models.BigAutoField(primary_key=True)
    id_number = models.CharField(max_length=14, unique=True, null=True, blank=True, verbose_name="الرقم القومي")
    date_of_birth = models.DateField(verbose_name="تاريخ الميلاد", null=True, blank=True)
    date_of_retirement = models.DateField(verbose_name="تاريخ التقاعد", null=True, blank=True)
    age = models.IntegerField(verbose_name="العمر", null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name="الاسم")
    mainornot = models.IntegerField(default=1)
    sort_number = models.IntegerField(null=True, blank=True)
    dep_sort = models.IntegerField(null=True, blank=True)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, related_name='employees')
    image = models.ImageField(upload_to='employee_images/', default='employee_images/noimage.jpg', null=True, blank=True)
    amen_or_ola = models.BooleanField(default=0)
    rank = models.ForeignKey(Rank, on_delete=models.SET_NULL, null=True, blank=True)
    rank_kind = models.IntegerField(null=True, blank=True)
    nickname = models.CharField(max_length=255, null=True, blank=True)
    operation = models.CharField(max_length=20, choices=OPERATION_CHOICES, default='لم يحدد', null=True, blank=True)
    police_number = models.CharField(max_length=255, null=True, blank=True)
    insurance_number = models.CharField(max_length=255, null=True, blank=True)
    date_of_edara = models.DateField(null=True, blank=True)
    date_of_appointment = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    alt_phone_number = models.CharField(max_length=255, null=True, blank=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, null=True, blank=True)
    gender = models.CharField(max_length=255, null=True, blank=True)
    governorate = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    health_status = models.CharField(max_length=255, choices=HEALTH_STATUS_CHOICES, null=True, blank=True)
    tmamam = models.IntegerField(default=1)
    food = models.IntegerField(default=1)
    rahatcounter = models.IntegerField(default=0)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    total_leave = models.IntegerField(default=0)
    bus = models.IntegerField(default=1)
    nots = models.TextField(null=True, blank=True, verbose_name="ملاحظات")
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        db_table = 'employees'

    def extract_birth_date(self):
        if not self.id_number or len(self.id_number) != 14 or not self.id_number.isdigit():
            return None
        
        century_digit = self.id_number[0]
        year = self.id_number[1:3]
        month = self.id_number[3:5]
        day = self.id_number[5:7]

        if century_digit == '2':
            full_year = f"19{year}"
        elif century_digit == '3':
            full_year = f"20{year}"
        else:
            return None

        try:
            return datetime.strptime(f"{full_year}-{month}-{day}", "%Y-%m-%d").date()
        except ValueError:
            return None

    def __str__(self):
        return self.name