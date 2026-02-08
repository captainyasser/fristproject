from django.db import models

class SystemSetting(models.Model):
    # This model will typically have only one row
    late_notification_days = models.PositiveIntegerField(
        default=3,
        verbose_name="مدة انذار التنبيهات المتاخره (بالأيام)"
    )

    def save(self, *args, **kwargs):
        # Singleton pattern: ensure only one instance exists
        if not self.pk and SystemSetting.objects.exists():
            # If trying to create a new instance and one already exists,
            # update the existing one instead (optional behavior)
            # or raise an error. Here we just update the first one.
            existing = SystemSetting.objects.first()
            existing.late_notification_days = self.late_notification_days
            return existing.save(*args, **kwargs)
        return super(SystemSetting, self).save(*args, **kwargs)

    def __str__(self):
        return "إعدادات النظام"

    class Meta:
        verbose_name = "إعدادات النظام"
        verbose_name_plural = "إعدادات النظام"
