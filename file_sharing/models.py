from django.db import models
from django.conf import settings

class SharedFile(models.Model):
    file = models.FileField(upload_to='shared_files/%Y/%m/%d/')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} (uploaded by {self.user.username})"