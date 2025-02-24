from django.db import models
from institutes.models import Institute  # تأكد من استيراد المعهد
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, related_name="users", null=True, blank=True)

    def __str__(self):
        return f"{self.username} - {self.institute.name if self.institute else 'No Institute'}"
