from django.db import models

class Rank(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="اسم الدرجة")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "الدرجة"
        verbose_name_plural = "الدرجات"
        ordering = ["id"]  # ترتيب الدرجات تصاعديًا
