from django.db import models

class Task(models.Model):
    REPEAT_CHOICES = [
        ('none', 'غير متكررة'),
        ('daily', 'يومي'),
        ('monthly', 'شهري'),
        ('quarterly', 'كل 3 أشهر'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()  # تغيير إلى DateField بدلاً من DateTimeField
    is_completed = models.BooleanField(default=False)
    repeat = models.CharField(max_length=10, choices=REPEAT_CHOICES, default='none')

    def __str__(self):
        return self.title