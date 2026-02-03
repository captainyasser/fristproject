# education/models.py
from django.db import models
from em_data.models import Employee  # مسار الـ Employee كما عندك
from django.utils import timezone

LEVEL_CHOICES = [
    ('عالي', 'عالي'),
    ('فوق متوسط', 'فوق متوسط'),
    ('متوسط', 'متوسط'),
    ('إعدادي', 'إعدادي'),
    ('إبتدائي', 'إبتدائي'),
]

TYPE_CHOICES = [
    ('ليسانس حقوق', 'ليسانس حقوق'),
    ('دبلوم تجارة', 'دبلوم تجارة'),
    ('دبلوم صناعي', 'دبلوم صناعي'),
    ('دبلوم زراعي', 'دبلوم زراعي'),
    ('الإعدادية', 'الإعدادية'),
    ('الإبتدائية', 'الإبتدائية'),
    ('غير ذلك', 'غير ذلك'),
]

GRADE_CHOICES = [
    ('إمتياز', 'إمتياز'),
    ('جيد جدا', 'جيد جدا'),
    ('جيد', 'جيد'),
    ('مقبول', 'مقبول'),
    ('ضعيف', 'ضعيف'),
]

class Education(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='educations', null=False, blank=False)
    decision_number = models.CharField("رقم قرار الموافقة", max_length=255, null=True, blank=True)
    university_name = models.CharField("اسم الجامعة", max_length=255, null=True, blank=True)
    level = models.CharField("مستوى المؤهل", max_length=50, choices=LEVEL_CHOICES, null=True, blank=True)
    qualification_type = models.CharField("نوع المؤهل", max_length=255, choices=TYPE_CHOICES, null=True, blank=True)
    grade = models.CharField("التقدير", max_length=50, choices=GRADE_CHOICES, null=True, blank=True)
    obtained_date = models.DateField("تاريخ الحصول", null=True, blank=True)
    degree_validation_image = models.ImageField("صورة صحة المؤهل", upload_to='education/validation/', null=True, blank=True)
    degree_image = models.ImageField("صورة الشهادة", upload_to='education/degrees/', null=True, blank=True)
    ministry_approval_image = models.ImageField("صورة موافقة الوزارة", upload_to='education/approvals/', null=True, blank=True)
    notes = models.TextField("ملاحظات", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'education'
        verbose_name = 'مؤهل'
        verbose_name_plural = 'المؤهلات'

    def __str__(self):
        return f"{self.employee.name} - {self.qualification_type or 'مؤهل غير محدد'}"
