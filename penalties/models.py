# F:\emapi-edit\myproject\penalties\models.py
from django.db import models
from django.conf import settings
from em_data.models import Employee

# =========================
# أنواع الجزاءات
# =========================
class PenaltyLevel(models.Model):
    name = models.CharField(max_length=50, verbose_name="اسم النوع")
    description = models.TextField(blank=True, null=True, verbose_name="الوصف")
    is_major = models.BooleanField(default=False, verbose_name="جزاء كبرى؟")
    order = models.IntegerField(default=0, verbose_name="ترتيب العرض")
    is_active = models.BooleanField(default=True, verbose_name="مفعل")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "نوع الجزاء"
        verbose_name_plural = "أنواع الجزاءات"


# =========================
# الجزاءات الموقعة
# =========================
class PenaltyApplied(models.Model):
    name = models.CharField(max_length=150, verbose_name="اسم الجزاء الموقع")
    penalty_level = models.ForeignKey(
        PenaltyLevel,
        on_delete=models.CASCADE,
        related_name='applied_penalties',
        verbose_name="نوع الجزاء المرتبط"
    )
    description = models.TextField(blank=True, null=True, verbose_name="الوصف")
    is_active = models.BooleanField(default=True, verbose_name="مفعل")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "الجزاء الموقع"
        verbose_name_plural = "الجزاءات الموقعة"


# =========================
# مقدار الجزاء (اختياري لكل جزاء موقع)
# =========================
from django.db import models

class PenaltyAmount(models.Model):
    penalty_applied = models.ForeignKey(
        PenaltyApplied,
        on_delete=models.CASCADE,
        related_name='amounts',
        verbose_name="الجزاء الموقع"
    )
    name = models.CharField(max_length=100, verbose_name="اسم مقدار الجزاء")
    value = models.DecimalField(max_digits=5, decimal_places=2, default=1, verbose_name="القيمة")  # يقبل كسور مثل 0.25، 0.5
    is_active = models.BooleanField(default=True, verbose_name="مفعل")

    def __str__(self):
        return f"{self.penalty_applied.name} - {self.name}"

    class Meta:
        verbose_name = "مقدار الجزاء"
        verbose_name_plural = "مقادير الجزاءات"



# =========================
# تصنيفات المخالفات
# =========================
class ViolationCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="اسم التصنيف")
    description = models.TextField(blank=True, null=True, verbose_name="شرح التصنيف")
    is_active = models.BooleanField(default=True, verbose_name="مفعل")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "تصنيف المخالفة"
        verbose_name_plural = "تصنيفات المخالفات"


# =========================
# أنواع المخالفات
# =========================
class ViolationType(models.Model):
    name = models.CharField(max_length=150, verbose_name="اسم المخالفة")
    category = models.ForeignKey(
        ViolationCategory,
        on_delete=models.CASCADE,
        related_name='violation_types',
        verbose_name="التصنيف"
    )
    description_template = models.TextField(
        blank=True, null=True,
        verbose_name="قالب وصف المخالفة",
        help_text="يمكنك استخدام {date} وسيتم استبداله بتاريخ اليوم"
    )
    is_absence = models.BooleanField(default=False, verbose_name="هل هي مخالفة غياب؟")
    is_active = models.BooleanField(default=True, verbose_name="مفعل")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "نوع المخالفة"
        verbose_name_plural = "أنواع المخالفات"


# =========================
# سجلات الجزاءات
# =========================
class PenaltyRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='penalties', verbose_name="الفرد")
    penalty_date = models.DateField(verbose_name="تاريخ الجزاء")

    # العلاقات
    penalty_level = models.ForeignKey(PenaltyLevel, on_delete=models.SET_NULL, null=True, verbose_name="نوع الجزاء")
    penalty_applied = models.ForeignKey(PenaltyApplied, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="الجزاء الموقع")
    penalty_amount = models.ForeignKey(PenaltyAmount, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="مقدار الجزاء")
    category = models.ForeignKey(ViolationCategory, on_delete=models.SET_NULL, null=True, verbose_name="التصنيف")
    violation_type = models.ForeignKey(ViolationType, on_delete=models.SET_NULL, null=True, verbose_name="نوع المخالفة")
    violation_description = models.TextField(blank=True, null=True, verbose_name="وصف المخالفة")
    notes = models.TextField(blank=True, null=True, verbose_name="ملاحظات")

    # الغياب
    absence_code = models.CharField(max_length=50, blank=True, null=True, verbose_name="بند الغياب")
    attendance_code = models.CharField(max_length=50, blank=True, null=True, verbose_name="بند الحضور")

    # صورة الأورنيك
    form_image = models.ImageField(upload_to='penalty_forms/', blank=True, null=True, verbose_name="صورة الأورنيك")

    # محو الجزاءات
    erase_date = models.DateField(blank=True, null=True, verbose_name="تاريخ محو الجزاء")
    erase_decision_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="رقم قرار المحو")
    erase_year = models.IntegerField(blank=True, null=True, verbose_name="سنة المحو")
    erase_notes = models.TextField(blank=True, null=True, verbose_name="ملاحظات المحو")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإدخال")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="المستخدم المدخل")

    def __str__(self):
        return f"{self.employee} - {self.penalty_date}"

    class Meta:
        verbose_name = "سجل الجزاء"
        verbose_name_plural = "سجلات الجزاءات"


# =========================
# نصوص جاهزة للمخالفات
# =========================
class ViolationPreset(models.Model):
    name = models.CharField(max_length=150, verbose_name="العنوان التعريفي")
    text = models.TextField(verbose_name="نص المخالفة")
    violation_type = models.ForeignKey(ViolationType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="نوع المخالفة المرتبط", help_text="اختياري: لربط النص بنوع مخالفة محدد")
    is_active = models.BooleanField(default=True, verbose_name="مفعل")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "نص مخالفة جاهز"
        verbose_name_plural = "نصوص مخالفات جاهزة"
