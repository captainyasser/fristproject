from django.db import models

from institutes.models import Institute



class Employee(models.Model):
    # Rank Choices
    RANK_CHOICES = [
        ('أمين شرطة ممتاز أول', 'أمين شرطة ممتاز أول'),
        ('أمين شرطة ممتاز ثان', 'أمين شرطة ممتاز ثان'),
        ('أمين شرطة ممتاز', 'أمين شرطة ممتاز'),
        ('أمين شرطة أول', 'أمين شرطة أول'),
        ('أمين شرطة ثان', 'أمين شرطة ثان'),
        ('أمين شرطة ثالث', 'أمين شرطة ثالث'),
        ('مساعد شرطة ممتاز', 'مساعد شرطة ممتاز'),
        ('مساعد شرطة أول', 'مساعد شرطة أول'),
        ('مساعد شرطة ثان', 'مساعد شرطة ثان'),
        ('مساعد شرطة ثالث', 'مساعد شرطة ثالث'),
        ('مراقب شرطة ممتاز', 'مراقب شرطة ممتاز'),
        ('مراقب شرطة أول', 'مراقب شرطة أول'),
        ('مراقب شرطة ثان', 'مراقب شرطة ثان'),
        ('مراقب شرطة ثالث', 'مراقب شرطة ثالث'),
        ('مندوب شرطة ممتاز', 'مندوب شرطة ممتاز'),
        ('مندوب شرطة أول', 'مندوب شرطة أول'),
        ('مندوب شرطة ثان', 'مندوب شرطة ثان'),
        ('مندوب شرطة ثالث', 'مندوب شرطة ثالث'),
        ('رقيب أول', 'رقيب أول'),
        ('رقيب', 'رقيب'),
        ('عريف', 'عريف'),
        ('جندي', 'جندي'),
        ('معاون أمن ممتاز أول', 'معاون أمن ممتاز أول'),
        ('معاون أمن ممتاز ثان', 'معاون أمن ممتاز ثان'),
        ('معاون أمن ممتاز', 'معاون أمن ممتاز'),
        ('معاون أمن أول', 'معاون أمن أول'),
        ('معاون أمن ثان', 'معاون أمن ثان'),
        ('معاون أمن ثالث', 'معاون أمن ثالث'),
    ]

    # Fields
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, related_name="employees")  # ربط الموظف بالمعهد
    rank = models.CharField(max_length=255, choices=RANK_CHOICES, null=True, blank=True)
    sort_number = models.IntegerField(null=True, blank=True)
    police_number = models.CharField(max_length=255, null=True, blank=True)
    insurance_number = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_appointment = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'employees'

    def __str__(self):
        return f"{self.name} ({self.institute.name})"  # يظهر اسم الموظف والمعهد التابع له
