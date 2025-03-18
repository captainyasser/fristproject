from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Promotion
import logging

logger = logging.getLogger(__name__)

# تعليق الإشارة إذا لم تكن ضرورية
# @receiver(post_save, sender=Promotion)
# def update_employee_rank(sender, instance, created, update_rank=None, **kwargs):
#     logger.info("Signal triggered: created=%s, update_rank=%s", created, update_rank)
#     if created and update_rank == 'yes':
#         logger.info("Updating rank for employee %s to %s", instance.employee.id, instance.to_rank.id)
#         instance.employee.rank = instance.to_rank
#         instance.employee.save(update_fields=['rank'])
#     else:
#         logger.info("Rank not updated: created=%s, update_rank=%s", created, update_rank)