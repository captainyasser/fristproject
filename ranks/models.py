from django.db import models

class Rank(models.Model):
    RANK_TYPES = (
        ('primary', 'درجة أولى'),
        ('police_officer', 'أمين شرطة'),
        ('security_assistant', 'معاون أمن'),
    )

    name = models.CharField(max_length=255, unique=True, verbose_name="اسم الدرجة")
    rank_type = models.CharField(
        max_length=20,
        choices=RANK_TYPES,
        verbose_name="نوع الدرجة",
        help_text="اختر نوع الدرجة (أولى، أمين شرطة، معاون أمن)"
    )
    order = models.PositiveIntegerField(
        default=1,
        verbose_name="الترتيب",
        help_text="رقم يحدد ترتيب الدرجة (1 = درجة أدنى)"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="نشط",
        help_text="حدد ما إذا كانت الدرجة مستخدمة حاليًا"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "الدرجة"
        verbose_name_plural = "الدرجات"
        ordering = ["order"]

    def get_next_rank(self):
        """دالة للحصول على الدرجة التالية في نفس النوع"""
        return Rank.objects.filter(
            rank_type=self.rank_type,
            order__gt=self.order,
            is_active=True
        ).order_by('order').first()