from django.contrib import admin
from .models import SecretReport

@admin.register(SecretReport)
class SecretReportAdmin(admin.ModelAdmin):
    list_display = ('employee', 'year', 'score', 'created_at')
    search_fields = ('employee__name', 'year')
    list_filter = ('year',)
