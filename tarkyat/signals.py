from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Promotion

@receiver(post_save, sender=Promotion)
def update_employee_rank(sender, instance, created, **kwargs):
    if created:  # يتم التحديث فقط عند إنشاء سجل جديد
        instance.employee.rank = instance.to_rank
        instance.employee.save()