from django.db import models

class Task(models.Model):
    REPEAT_CHOICES = [
        ('none', 'غير متكررة'),
        ('daily', 'يومي'),
        ('monthly', 'شهري'),
        ('quarterly', 'كل 3 أشهر'),
    ]

    title = models.CharField(max_length=200)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    repeat_type = models.CharField(max_length=10, choices=REPEAT_CHOICES, default='none')
    repeat_interval = models.PositiveIntegerField(default=1)
    reminder_days = models.PositiveIntegerField(default=0)
    is_muted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class TaskFile(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='task_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File for {self.task.title}"