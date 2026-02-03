# elawat_tashgeea/admin.py
from django.contrib import admin
from .models import ElawaRecord

@admin.register(ElawaRecord)
class ElawaRecordAdmin(admin.ModelAdmin):
    list_display = ('employee', 'decision_number', 'elawa_date', 'created_at')
    search_fields = ('employee__name', 'decision_number')
    list_filter = ('elawa_date',)
