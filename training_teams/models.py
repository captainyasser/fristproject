from django.db import models
from django.core.exceptions import ValidationError
from em_data.models import Employee  # استيراد نموذج Employee من تطبيق em_data

class TrainingTeam(models.Model):
    name = models.CharField(max_length=100, verbose_name="اسم الفريق التدريبي")
    description = models.TextField(blank=True, null=True, verbose_name="الوصف")

    def __str__(self):
        return self.name

class Places(models.Model):
    name = models.CharField(max_length=100, verbose_name="اسم المكان")
    description = models.TextField(blank=True, null=True, verbose_name="الوصف")
    address = models.TextField(blank=True, null=True, verbose_name="العنوان")  

    def __str__(self):
        return self.name

class EmTrainingTeams(models.Model):
    RESULT_CHOICES = [
        ('ناجح', 'ناجح'),
        ('راسب', 'راسب'),
    ]

    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, 
        related_name='training_teams', verbose_name="الموظف"
    )
    name = models.CharField(max_length=100, verbose_name="اسم التدريب")
    training_team = models.ForeignKey(
        TrainingTeam, on_delete=models.CASCADE, 
        related_name='em_training_teams', verbose_name="فريق التدريب"
    )
    place = models.ForeignKey(
        Places, on_delete=models.CASCADE, 
        related_name='em_training_teams', verbose_name="المكان"
    )
    start_date = models.DateField(verbose_name="تاريخ البدء")
    end_date = models.DateField(verbose_name="تاريخ الانتهاء")
    result = models.CharField(
        max_length=10, choices=RESULT_CHOICES, 
        blank=True, null=True, verbose_name="النتيجة"
    )
    note = models.TextField(verbose_name="ملاحظات", default="")
    round_num = models.IntegerField(blank=True, null=True, verbose_name="رقم الدورة")

    class Meta:
        verbose_name = "فريق تدريبي"
        verbose_name_plural = "الفرق التدريبية"
        ordering = ['-start_date']  # ترتيب الفرق من الأحدث إلى الأقدم
        constraints = [
            models.UniqueConstraint(
                fields=['employee', 'training_team', 'start_date', 'end_date'],
                name="unique_employee_training_period"
            )
        ]

    def clean(self):
        """ التحقق من أن تاريخ الانتهاء لا يكون قبل تاريخ البدء """
        if self.end_date < self.start_date:
            raise ValidationError("تاريخ الانتهاء لا يمكن أن يكون قبل تاريخ البدء.")

    def __str__(self):
        return f"{self.name} - {self.employee.nickname}"  # إذا كان Employee لديه حقل `nickname`
